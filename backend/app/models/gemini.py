from pydantic import BaseModel, Field

from app.models.news import NewsArticle


class GeminiSummaryRequest(BaseModel):
    articles: list[NewsArticle] = Field(..., min_length=1, description="News articles to summarize")


class GeminiSummaryResponse(BaseModel):
    main_events: list[str]
    key_facts: list[str]
    future_implications: list[str]
    expert_opinions: list[str]

