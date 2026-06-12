from pydantic import BaseModel, Field


class PodcastScriptRequest(BaseModel):
    structured_summary: dict[str, list[str]] = Field(
        ..., description="Structured summary with main_events, key_facts, future_implications, and expert_opinions"
    )
    topic: str | None = Field(default=None, description="Optional topic for contextual framing")
    conversation_minutes: int = Field(default=6, ge=5, le=7)


class PodcastScriptResponse(BaseModel):
    host_a: str
    host_b: str
    full_script: str
    estimated_duration_minutes: int
