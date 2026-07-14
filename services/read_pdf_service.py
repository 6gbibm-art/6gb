import pymupdf
from fastapi import HTTPException, UploadFile
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
        pages.append(page.get_text())
    document.close()
    text = "\n".join(pages).strip()
    if not text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the PDF."
        )
    return text