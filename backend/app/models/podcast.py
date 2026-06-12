from datetime import datetime

from pydantic import AnyUrl, BaseModel, Field


class PodcastGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200, description="Topic to fetch news for")
    article_limit: int = Field(default=5, ge=1, le=20)
    language: str = Field(default="en", min_length=2, max_length=10)


class PodcastSource(BaseModel):
    title: str
    url: AnyUrl
    source_name: str
    published_at: datetime
    snippet: str


class PodcastTranscript(BaseModel):
    host_a: str
    host_b: str
    full_script: str


class PodcastMetadata(BaseModel):
    article_count: int
    generated_at: datetime
    provider_name: str


class PodcastGenerateResponse(BaseModel):
    request_id: str
    topic: str
    sources: list[PodcastSource]
    summary: str
    transcript: PodcastTranscript
    audio_url: str
    metadata: PodcastMetadata