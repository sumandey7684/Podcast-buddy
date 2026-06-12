from pydantic import BaseModel, Field


class TextToSpeechRequest(BaseModel):
    podcast_transcript: str = Field(..., min_length=1, description="Transcript containing HOST_A and HOST_B labels")
    output_filename: str = Field(default="podcast.mp3", description="Output MP3 filename")


class TextToSpeechResponse(BaseModel):
    output_filename: str
    output_path: str
    segment_count: int
    speaker_voices: dict[str, str]
