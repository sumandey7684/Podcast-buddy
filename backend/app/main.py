from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config.settings import get_settings
from app.routes.health import router as health_router
from app.routes.gemini import router as gemini_router
from app.routes.news import router as news_router
from app.routes.podcast import router as podcast_router
from app.routes.tts import router as tts_router


settings = get_settings()
STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
AUDIO_DIR = STATIC_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="Backend API for Podcast Buddy",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(news_router, prefix="/api/v1")
app.include_router(gemini_router, prefix="/api/v1")
app.include_router(podcast_router, prefix="/api/v1")
app.include_router(tts_router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "Podcast Buddy backend is running",
        "docs": "/docs",
    }
