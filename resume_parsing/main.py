import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from resume_routes import router as resume_router

load_dotenv()

app = FastAPI(
    title="RADIX Resume Parsing API",
    description="Extracts skills from PDF/DOCX resumes into the shared RADIX JSON contract.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router, prefix="/api/resume-parsing", tags=["Resume Parsing"])


@app.get("/")
def root():
    return {
        "service": "RADIX Resume Parsing API",
        "status": "running",
        "docs": "/docs",
        "analyze_endpoint": "POST /api/resume-parsing/analyze",
    }



