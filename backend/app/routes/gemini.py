from fastapi import APIRouter, HTTPException, status

from app.models.gemini import GeminiSummaryRequest, GeminiSummaryResponse
from app.services.gemini_service import GeminiService, GeminiServiceError

router = APIRouter(prefix="/gemini", tags=["gemini"])
gemini_service = GeminiService()


@router.post(
    "/summarize",
    response_model=GeminiSummaryResponse,
    status_code=status.HTTP_200_OK,
)
async def summarize_articles(request: GeminiSummaryRequest) -> GeminiSummaryResponse:
    try:
        return await gemini_service.summarize_articles(request)
    except GeminiServiceError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
