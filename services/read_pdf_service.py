import pymupdf
from fastapi import HTTPException, UploadFile
from services.pdf_parser import parse_page
async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Raises:
        HTTPException:
            400 - Invalid file type.
            400 - Invalid/corrupted PDF.
            400 - No readable text found.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400,detail="Only PDF files are accepted.")
    pdf_bytes = await file.read()
    try:
        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF."
        )
    pages = []
    for page in document:

        page_dict = page.get_text("dict")

        pages.append(
            parse_page(page_dict)
        )

    document.close()

    text = "\n\n".join(pages).strip()
    if not text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the PDF."
        )
    return text