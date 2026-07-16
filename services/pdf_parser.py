from collections import Counter
import re
import unicodedata

def get_body_font_size(page_dict: dict) -> float:
    """
    Finds the most common font size in the document.
    This is assumed to be the body text size.
    """

    sizes = []

    for block in page_dict["blocks"]:

        if block["type"] != 0:
            continue

        for line in block["lines"]:

            for span in line["spans"]:

                text = span["text"].strip()

                if text:

                    sizes.append(round(span["size"], 1))

    if not sizes:
        return 11.0

    return Counter(sizes).most_common(1)[0][0]
def detect_headings(elements):
    """
    Determines headings using relative font size and surrounding context.

    This avoids assuming that every bold line is a heading.
    """

    if not elements:
        return elements

    body_size = Counter(
        round(e["size"], 1)
        for e in elements
    ).most_common(1)[0][0]

    for i, element in enumerate(elements):

        text = element["text"].strip()

        if not text:
            continue

        # Very short lines are more likely headings
        word_count = len(text.split())

        larger_font = element["size"] >= body_size * 1.15

        bold = element["bold"]

        short = word_count <= 8
        uppercase = (

            text.isupper()

            and len(text) > 2

        )

        previous_gap = 999

        next_gap = 999

        if i > 0:
            previous_gap = (
                element["y"] -
                elements[i - 1]["y"]
            )

        if i < len(elements) - 1:
            next_gap = (
                elements[i + 1]["y"] -
                element["y"]
            )

        separated = (
            previous_gap > 18
            or next_gap > 18
        )

        element["is_heading"] = (

            (
                larger_font
                and short
                and separated
            )

            or

            (
                bold
                and larger_font
                and short
            )

            or

            uppercase

        )

    return elements

def extract_elements(page_dict: dict):
    """
    Converts the PyMuPDF page dictionary into ordered text elements.

    Returns:

    [
        {
            "text": "...",
            "size": 11,
            "bold": False,
            "x": 72,
            "y": 145
        }
    ]
    """

    elements = []


    for block in page_dict["blocks"]:

        if block["type"] != 0:
            continue

        for line in block["lines"]:

            spans = line["spans"]

            if not spans:
                continue

            text = " ".join(

                span["text"].strip()

                for span in spans

                if span["text"].strip()

            ).strip()

            if not text:
                continue

            first = spans[0]

            font = first["font"].lower()

            bold = "bold" in font

            elements.append({

                "text": text,

                "size": first["size"],

                "bold": bold,

                "x": first["bbox"][0],

                "y": first["bbox"][1],

                "is_heading":
                    False

            })

    elements.sort(

        key=lambda e: (

            round(e["y"], 1),

            e["x"]

        )

    )

    return elements

def merge_paragraphs(elements):
    """
    Merges consecutive body-text lines into proper paragraphs while
    preserving headings and bullet lists.
    """

    merged = []

    paragraph = ""

    previous = None

    current_bullet = None

    for element in elements:

        text = element["text"].strip()

        # ------------------------------
        # Heading
        # ------------------------------

        if element["is_heading"]:

            if paragraph:

                merged.append({
                    "type": "paragraph",
                    "text": paragraph.strip()
                })

                paragraph = ""

            merged.append({
                "type": "heading",
                "text": text
            })

            previous = element

            continue

        # ------------------------------
        # Bullet List
        # ------------------------------

        if text.startswith((
            "•",
            "-",
            "*",
            "▪",
            "◦"
        )):

            if paragraph:

                merged.append({
                    "type": "paragraph",
                    "text": paragraph.strip()
                })

                paragraph = ""

            if current_bullet:

                merged.append({
                    "type": "bullet",
                    "text": current_bullet
                })

            current_bullet = text

            previous = element

            continue
        # -----------------------------------
        # Continue wrapped bullet
        # -----------------------------------

        if current_bullet:

            y_gap = element["y"] - previous["y"]

            x_shift = abs(
                element["x"] - previous["x"]
            )

            if y_gap < 20 and x_shift > 10:

                current_bullet += " " + text

                previous = element

                continue

            merged.append({
                "type": "bullet",
                "text": current_bullet
            })

            current_bullet = None
        # ------------------------------
        # First body line
        # ------------------------------

        if not paragraph:

            paragraph = text

            previous = element

            continue

        # ------------------------------
        # Decide whether this line belongs
        # to the same paragraph.
        # ------------------------------

        y_gap = element["y"] - previous["y"]

        x_shift = abs(
            element["x"] - previous["x"]
        )

        if y_gap < 22 and x_shift < 20:

            paragraph += " " + text

        else:

            merged.append({
                "type": "paragraph",
                "text": paragraph.strip()
            })

            paragraph = text

        previous = element

    if paragraph:

        merged.append({
            "type": "paragraph",
            "text": paragraph.strip()
        })
    if current_bullet:

        merged.append({
            "type": "bullet",
            "text": current_bullet
        })
    return merged

def render_markdown(elements):
    """
    Converts parsed elements into clean Markdown.
    """

    markdown = []

    for element in elements:

        element_type = element["type"]

        text = element["text"].strip()

        if not text:
            continue

        if element_type == "heading":

            markdown.append(f"\n## {text}\n")

        elif element_type == "bullet":

            bullet = text

            for symbol in (
                "•",
                "▪",
                "◦",
                "*"
            ):

                if bullet.startswith(symbol):

                    bullet = bullet[len(symbol):].strip()

                    break

            markdown.append(f"- {bullet}")

        else:

            markdown.append(text)

    return "\n\n".join(markdown)

def parse_page(page_dict):
    """
    Complete parsing pipeline.

    PyMuPDF Dict
            ↓
    Extract Elements
            ↓
    Merge Paragraphs
            ↓
    Markdown
    """

    elements = extract_elements(page_dict)

    elements = detect_headings(elements)

    merged = merge_paragraphs(elements)

    markdown = render_markdown(merged)
    with open("parsed_resume.md", "w", encoding="utf-8") as f:
        f.write(markdown)
    return clean_markdown(markdown)

def clean_markdown(markdown: str) -> str:
    """
    Final cleanup before sending text to Gemini.
    Performs generic Unicode normalization and whitespace cleanup.
    """

    # Normalize Unicode representation
    markdown = unicodedata.normalize("NFKC", markdown)

    # Common ligatures produced by PDFs
    ligatures = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬀ": "ff",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
    }

    for bad, good in ligatures.items():
        markdown = markdown.replace(bad, good)

    # Normalize whitespace
    markdown = markdown.replace("\t", " ")

    markdown = re.sub(r"[ ]{2,}", " ", markdown)

    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    return markdown.strip()