import io

from docx import Document
from fastapi.responses import StreamingResponse


def create_docx(
    content: str,
    title: str,
    filename: str
) -> StreamingResponse:
    """
    Generate a DOCX document.

    Args:
        content: Document body.
        title: Heading displayed at the top.
        filename: Download filename.
    """

    document = Document()

    document.add_heading(title, level=1)

    for paragraph in content.split("\n"):

        if paragraph.strip():

            document.add_paragraph(paragraph)

    buffer = io.BytesIO()

    document.save(buffer)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        }
    )