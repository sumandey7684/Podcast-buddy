from fastapi import APIRouter, HTTPException, status

from app.models.podcast import PodcastGenerateRequest, PodcastGenerateResponse
from app.services.podcast_service import PodcastService

router = APIRouter(prefix="/podcast", tags=["podcast"])
podcast_service = PodcastService()


@router.post(
    "/generate",
    response_model=PodcastGenerateResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_podcast(request: PodcastGenerateRequest) -> PodcastGenerateResponse:
    try:
        return await podcast_service.generate(request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc