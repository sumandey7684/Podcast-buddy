from fastapi import APIRouter, HTTPException, status

from app.models.tts import TextToSpeechRequest, TextToSpeechResponse
from app.services.tts_service import TextToSpeechService, TextToSpeechServiceError

router = APIRouter(prefix="/tts", tags=["tts"])
tts_service = TextToSpeechService()


@router.post(
    "/generate",
    response_model=TextToSpeechResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_audio(request: TextToSpeechRequest) -> TextToSpeechResponse:
    try:
        return await tts_service.generate_podcast_audio(request)
    except TextToSpeechServiceError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
