# Podcast Buddy Backend

FastAPI backend scaffold for the Podcast Buddy hackathon project.

## Stack

- Python 3.12
- FastAPI
- Pydantic v2
- Uvicorn

## Structure

- `app/main.py`: FastAPI application entrypoint
- `app/routes/`: API route handlers
- `app/services/`: orchestration and business logic
- `app/models/`: request and response schemas
- `app/config/`: environment and settings
- `app/utils/`: reusable helper functions

## Endpoints

- `GET /health`: health check
- `POST /api/v1/news/search`: fetch latest GNews articles for a topic
- `POST /api/v1/gemini/summarize`: summarize articles into structured podcast insights
- `POST /api/v1/podcast/generate`: generate a podcast payload for a topic
- `POST /api/v1/tts/generate`: convert a HOST_A/HOST_B transcript into a merged MP3

## Example usage

Request:

```json
{
	"topic": "Artificial Intelligence",
	"limit": 10,
	"language": "en"
}
```

Response fields:

- `title`
- `description`
- `source`
- `url`
- `published_at`

The route is designed as a thin controller. All GNews logic lives in `app/services/news_service.py`, and the Pydantic contracts live in `app/models/news.py`.

## Gemini usage

Request:

```json
{
	"articles": [
		{
			"title": "Article title",
			"description": "Short description",
			"source": "Publication",
			"url": "https://example.com/article",
			"published_at": "2026-06-12T10:00:00Z"
		}
	]
}
```

Response:

```json
{
	"main_events": [],
	"key_facts": [],
	"future_implications": [],
	"expert_opinions": []
}
```

## Podcast Script Generator

Input:

```json
{
	"topic": "Artificial Intelligence",
	"conversation_minutes": 6,
	"structured_summary": {
		"main_events": ["AI regulation advanced in multiple regions"],
		"key_facts": ["New policies focus on transparency"],
		"future_implications": ["Companies may need stronger compliance"],
		"expert_opinions": ["Analysts expect faster adoption of governance frameworks"]
	}
}
```

Example output:

```json
{
	"host_a": "HOST_A: So the big story this week is...",
	"host_b": "HOST_B: Yeah, and what stands out to me is...",
	"full_script": "HOST_A: ...\nHOST_B: ...",
	"estimated_duration_minutes": 6
}
```

The implementation lives in `app/services/script_generator_service.py` and the prompt template is in `app/prompts/podcast_script_prompt.py`.

## Text to Speech

Input:

```json
{
	"podcast_transcript": "HOST_A: Welcome back...\nHOST_B: Great to be here...",
	"output_filename": "podcast.mp3"
}
```

Response:

```json
{
	"output_filename": "podcast.mp3",
	"output_path": "D:/.../podcast.mp3",
	"segment_count": 2,
	"speaker_voices": {
		"HOST_A": "voice_a_id",
		"HOST_B": "voice_b_id"
	}
}
```

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment

Copy `.env.example` to `.env` and set your API keys.