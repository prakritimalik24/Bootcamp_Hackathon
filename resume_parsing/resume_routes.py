from fastapi import APIRouter, File, UploadFile, HTTPException
from resume_controller import analyze_resume

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  


@router.post("/analyze")
async def analyze_resume_route(file: UploadFile = File(...)):
    filename = file.filename or "uploaded_resume"
    extension = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Upload a PDF or DOCX resume.",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File is too large. Maximum size is 10 MB.")

    try:
        return analyze_resume(filename=filename, file_bytes=file_bytes, extension=extension)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        # Avoid returning internal stack traces or secret values to clients.
        raise HTTPException(status_code=500, detail="Resume analysis failed. Check the server terminal.") from exc
