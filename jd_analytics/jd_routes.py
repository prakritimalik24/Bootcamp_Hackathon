
from fastapi import APIRouter, UploadFile, File

from jd_controller import analyze_jd

router = APIRouter()


@router.post("/analyze")
async def analyze_job_description(
    file: UploadFile = File(...)
):
    return await analyze_jd(file)
