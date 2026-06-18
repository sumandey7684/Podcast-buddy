from fastapi import APIRouter, HTTPException, status

from app.models.podcast import PodcastGenerateRequest, PodcastGenerateResponse
from app.services.audio_service import AudioServiceError
from app.services.gemini_service import GeminiServiceError
from app.services.news_service import NewsServiceError
from app.services.podcast_service import PodcastBadRequestError, PodcastExternalServiceError, PodcastService
from app.services.script_service import ScriptServiceError

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
    except PodcastBadRequestError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except (NewsServiceError, GeminiServiceError, ScriptServiceError, AudioServiceError, PodcastExternalServiceError) as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected podcast generation failure",
        ) from exc