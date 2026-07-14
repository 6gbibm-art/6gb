import io

from fastapi.responses import StreamingResponse

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
)


def create_pdf(
    content: str,
    title: str,
    filename: str
) -> StreamingResponse:
    """
    Generate a PDF document.

    Args:
        content: Text to place inside the PDF.
        title: Heading displayed at the top of the document.
        filename: Name of the downloaded PDF file.
    """

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(f"<b>{title}</b>", styles["Heading1"])
    )

    for paragraph in content.split("\n"):

        if paragraph.strip():

            safe_text = (
                paragraph.replace("&", "&amp;")
                         .replace("<", "&lt;")
                         .replace(">", "&gt;")
            )

            story.append(
                Paragraph(
                    safe_text,
                    styles["BodyText"]
                )
            )

    doc.build(story)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        }
    )