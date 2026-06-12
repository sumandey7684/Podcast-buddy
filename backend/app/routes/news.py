from fastapi import APIRouter, HTTPException, status

from app.models.news import NewsSearchRequest, NewsSearchResponse
from app.services.news_service import NewsService, NewsServiceError

router = APIRouter(prefix="/news", tags=["news"])
news_service = NewsService()


@router.post(
    "/search",
    response_model=NewsSearchResponse,
    status_code=status.HTTP_200_OK,
)
async def search_news(request: NewsSearchRequest) -> NewsSearchResponse:
    try:
        return await news_service.search_news(request)
    except NewsServiceError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc