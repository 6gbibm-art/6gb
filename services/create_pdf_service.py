import io
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)
from reportlab.lib.styles import (
    getSampleStyleSheet
)
from fastapi.responses import StreamingResponse
def create_pdf(letter: str) -> StreamingResponse:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []
    story.append(
        Paragraph("<b>Cover Letter</b>",styles["Heading1"]))
    for paragraph in letter.split("\n"):
        if paragraph.strip():
            story.append(
                Paragraph(
                    paragraph.replace("&", "&amp;")
                             .replace("<", "&lt;")
                             .replace(">", "&gt;"),

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
            'attachment; filename="Cover_Letter.pdf"'
        }
    )