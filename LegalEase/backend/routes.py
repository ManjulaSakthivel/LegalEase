from fastapi import APIRouter, Depends, HTTPException

from backend.config import get_settings
from backend.dependencies import get_generator
from backend.schemas import DocumentRequest, DocumentResponse
from backend.ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter(tags=["documents"])


@router.post("/generate", response_model=DocumentResponse)
def generate_document(
    request: DocumentRequest,
    generator: GeminiDocumentGenerator = Depends(get_generator),
) -> DocumentResponse:
    try:
        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )
        return DocumentResponse(
            document_type=request.document_type,
            content=content,
            model=generator.model,
            demo_mode=generator.demo_mode,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {exc}",
        ) from exc


@router.get("/health")
def health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": bool(settings.gemini_api_key),
        "model": settings.gemini_model,
    }
