from datetime import datetime

from pydantic import AnyUrl, BaseModel, Field


class NewsSearchRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200, description="Topic to search latest news for")
    limit: int = Field(default=10, ge=1, le=10, description="Maximum number of articles to return")
    language: str = Field(default="en", min_length=2, max_length=10)


class NewsArticle(BaseModel):
    title: str
    description: str | None = None
    source: str
    url: AnyUrl
    published_at: datetime | None = None


class NewsSearchResponse(BaseModel):
    topic: str
    total_results: int
    articles: list[NewsArticle]