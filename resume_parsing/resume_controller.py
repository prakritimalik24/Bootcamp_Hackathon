from resume_service import parse_resume


def analyze_resume(filename: str, file_bytes: bytes, extension: str) -> dict:
    """Controller layer: delegates extraction and LLM analysis to the service."""
    return parse_resume(filename=filename, file_bytes=file_bytes, extension=extension)
