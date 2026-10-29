
from fastapi import UploadFile, HTTPException

from jd_service import extract_text, analyze_jd as analyze_jd_service


async def analyze_jd(file: UploadFile):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please upload a file"
        )

    filename = file.filename

    if not filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    try:
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        jd_text = extract_text(file_bytes, filename)

        if not jd_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the document"
            )

        return analyze_jd_service(jd_text, filename)

    except HTTPException:
        raise

    except Exception as e:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"JD analysis failed: {str(e)}"
        )