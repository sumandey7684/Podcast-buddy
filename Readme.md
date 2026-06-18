# 🎙️ Podcast Buddy

Turn breaking news into natural podcast episodes powered by AI.

Podcast Buddy is an AI-powered news-to-podcast platform that fetches the latest news on any topic, summarizes it with Gemini, generates a natural two-host conversation, converts the script into realistic speech with Edge TTS, merges the audio with FFmpeg, and delivers a playable MP3 episode in the browser.

Inspired by Google NotebookLM Audio Overview and modern editorial media experiences.

---

## Features

- Latest news fetching using the GNews API
- AI-powered news summarization using Gemini 2.5 Flash
- Natural two-host podcast dialogue generation via a local script engine
- Realistic AI voice generation using Edge TTS
- Audio merging using FFmpeg
- Downloadable MP3 podcast episodes
- Interactive transcript viewer
- Editorial news source cards
- Clean, responsive UI for desktop and mobile

---

## Demo Flow

```text
User enters a topic
        ↓
Fetch latest news (GNews)
        ↓
Gemini summary
        ↓
Local dialogue generation
        ↓
Edge TTS
        ↓
FFmpeg audio merge
        ↓
episode_{request_id}.mp3
        ↓
Frontend audio player
```

---

## Example

### Input

```text
Artificial Intelligence
```

### Output

#### News Sources

Example sources returned by GNews may include:

- Reuters
- Phys.org
- Bloomberg
- TechCrunch

#### Summary

Structured summary sections:

- Main Events
- Key Facts
- Future Implications
- Expert Opinions

#### Podcast Transcript

```text
HOST_A: Welcome to Podcast Buddy. Today we are looking at Artificial Intelligence...

HOST_B: That is a useful starting point, because it gives us one clear thread to follow...

HOST_A: One important fact here is that...

HOST_B: What stands out to me is this perspective: ...
```

#### Audio

```text
/static/audio/episode_{request_id}.mp3
```

---

## Tech Stack

### Frontend

| Technology   | Purpose              |
| ------------ | -------------------- |
| Next.js 15   | Frontend framework   |
| React 19     | UI library           |
| TypeScript   | Type safety          |
| Tailwind CSS | Styling              |
| Axios        | API communication    |
| Lucide React | Icons                |

### Backend

| Technology        | Purpose              |
| ----------------- | -------------------- |
| FastAPI           | REST API             |
| Python 3.12+      | Backend runtime      |
| Pydantic v2       | Validation           |
| HTTPX             | Async HTTP requests  |
| Uvicorn           | ASGI server          |

### AI and Media Stack

| Technology          | Purpose              |
| ------------------- | -------------------- |
| GNews API           | News retrieval       |
| Google GenAI SDK    | Gemini integration   |
| Gemini 2.5 Flash    | News summarization   |
| Local script engine | Podcast dialogue     |
| Edge TTS            | Voice generation     |
| FFmpeg              | Audio merging        |

---

## Project Architecture

```text
┌──────────────┐
│ User Input   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ GNews API    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Gemini       │
│ Summary      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Script       │
│ Generator    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Edge TTS     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ FFmpeg       │
│ Audio Merge  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ episode.mp3  │
└──────────────┘
```

---

## Folder Structure

```text
Podcast Buddy
├── frontend
│   ├── app
│   ├── components
│   ├── lib
│   ├── types
│   └── public
│
├── backend
│   ├── app
│   │   ├── config
│   │   ├── models
│   │   ├── routes
│   │   ├── services
│   │   └── utils
│   ├── static
│   │   └── audio
│   └── tests
│
├── README.md
└── .gitignore
```

---

## Backend API Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

### Search News

```http
POST /api/v1/news/search
```

Request:

```json
{
  "topic": "Artificial Intelligence",
  "limit": 10,
  "language": "en"
}
```

---

### Summarize News

```http
POST /api/v1/gemini/summarize
```

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

---

### Generate Podcast

```http
POST /api/v1/podcast/generate
```

Request:

```json
{
  "topic": "Artificial Intelligence",
  "article_limit": 5,
  "language": "en"
}
```

Response:

```json
{
  "request_id": "uuid",
  "topic": "Artificial Intelligence",
  "sources": [],
  "summary": "{\"main_events\":[],\"key_facts\":[],\"future_implications\":[],\"expert_opinions\":[]}",
  "transcript": {
    "host_a": "...",
    "host_b": "...",
    "full_script": "..."
  },
  "audio_url": "/static/audio/episode_{request_id}.mp3",
  "metadata": {
    "article_count": 5,
    "generated_at": "2026-06-18T10:00:00Z",
    "provider_name": "gnews"
  }
}
```

Notes:

- `summary` is returned as a JSON string containing structured summary fields.
- The frontend currently sends `article_limit: 10` when generating a podcast.

---

### Generate TTS Audio

```http
POST /api/v1/tts/generate
```

Request:

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
  "output_path": "...",
  "segment_count": 2,
  "speaker_voices": {
    "HOST_A": "en-US-AndrewNeural",
    "HOST_B": "en-US-EmmaNeural"
  }
}
```

---

## Environment Variables

### Backend

Create:

```text
backend/.env
```

Add:

```env
GNEWS_API_KEY=your_gnews_api_key
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
EDGE_TTS_VOICE_A=en-US-AndrewNeural
EDGE_TTS_VOICE_B=en-US-EmmaNeural
AUDIO_BASE_URL=/static/audio
```

Copy from `backend/.env.example` as a starting point.

### Frontend

Create:

```text
frontend/.env.local
```

Add:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Copy from `frontend/.env.example` as a starting point.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/sumandey7684/Podcast-buddy.git
cd Podcast-buddy
```

---

### Backend Setup

```bash
cd backend
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and run:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend:

```text
http://localhost:8000
```

Swagger docs:

```text
http://localhost:8000/docs
```

Requirements:

- Python 3.12+
- FFmpeg installed and available on your PATH

---

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

## UI Inspiration

Podcast Buddy draws inspiration from:

- Google NotebookLM Audio Overview
- Perplexity Discover
- Financial Times editorial design
- NPR Podcasts

---

## Current Status

### Backend

- News retrieval: Complete
- AI summary: Complete
- Dialogue generation: Complete
- Edge TTS: Complete
- FFmpeg audio merge: Complete
- Static audio hosting: Complete

### Frontend

- Topic input and podcast generation flow: Complete
- Audio player with download and playback controls: Complete
- Transcript viewer: Complete
- Waveform player: Planned
- Episode library: Planned

---

## Future Improvements

- Multi-language podcasts
- Multiple voice options
- Background music
- Podcast history
- User authentication
- Spotify integration
- Cloud audio storage
- Podcast sharing links

---

## Authors

- **Suman Dey**
- **Subhasish Rath**
- **Soumya Ranjan Samal**
- **Gaurav Kumar Nayak**

---

## License

MIT License. Add a `LICENSE` file to the repository if you want the license claim to be fully enforceable on GitHub.
