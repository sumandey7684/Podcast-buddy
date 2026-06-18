# 🎙️ Podcast Buddy

Turn breaking news into natural podcast episodes powered by AI.

Podcast Buddy is an AI-powered news-to-podcast platform that automatically fetches the latest news on any topic, summarizes it, generates a natural two-host conversation, converts the script into realistic speech, and delivers a playable podcast episode.

Inspired by Adobe Podcast, Google NotebookLM Audio Overview, and modern editorial media experiences.

---

## Features

* Latest news fetching using GNews API
* AI-powered news summarization using Gemini
* Natural two-host podcast conversation generation
* Realistic AI voice generation using Edge TTS
* Audio merging using FFmpeg
* Downloadable MP3 podcast episodes
* Interactive transcript viewer
* Editorial news source cards
* Modern Adobe Podcast-inspired UI
* Responsive design for desktop and mobile

---

## Demo Flow

```text
User enters a topic

↓

Fetch Latest News

↓

Gemini Summary

↓

Local Dialogue Generation

↓

Edge TTS

↓

FFmpeg Audio Merge

↓

episode.mp3

↓

Frontend Audio Player
```

---

## Example

### Input

```text
Artificial Intelligence
```

### Output

#### News Sources

* Reuters
* Phys.org
* Bloomberg
* TechCrunch

#### Summary

* Main Events
* Key Facts
* Future Implications
* Expert Opinions

#### Podcast Transcript

```text
HOST_A:

Welcome back to Podcast Buddy.
Today we're discussing Artificial Intelligence.

HOST_B:

Several important developments have emerged this week.

HOST_A:

AI voice cloning technology is becoming increasingly realistic.

HOST_B:

This raises important questions about digital identity and security.
```

#### Audio

```text
episode_xxxxx.mp3
```

---

# Tech Stack

## Frontend

| Technology    | Purpose            |
| ------------- | ------------------ |
| Next.js 15    | Frontend Framework |
| TypeScript    | Type Safety        |
| TailwindCSS   | Styling            |
| Axios         | API Communication  |
| Framer Motion | Animations         |

---

## Backend

| Technology  | Purpose             |
| ----------- | ------------------- |
| FastAPI     | REST API            |
| Python 3.14 | Backend Runtime     |
| Pydantic    | Validation          |
| HTTPX       | Async HTTP Requests |

---

## AI & Media Stack

| Technology          | Purpose            |
| ------------------- | ------------------ |
| GNews API           | News Retrieval     |
| Gemini 2.5 Flash    | News Summarization |
| Local Script Engine | Podcast Dialogue   |
| Edge TTS            | Voice Generation   |
| FFmpeg              | Audio Merging      |

---

# Project Architecture

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

# Folder Structure

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
│   │
│   ├── static
│   │   └── audio
│   │
│   └── tests
│

├── README.md

└── .gitignore
```

---

# Backend API Endpoints

## Health Check

```http
GET /health
```

Response

```json
{
  "status":"ok"
}
```

---

## Search News

```http
POST /api/v1/news/search
```

Request

```json
{
  "topic":"Artificial Intelligence",
  "limit":5,
  "language":"en"
}
```

---

## Summarize News

```http
POST /api/v1/gemini/summarize
```

Request

```json
{
  "articles":[]
}
```

---

## Generate Podcast

```http
POST /api/v1/podcast/generate
```

Request

```json
{
  "topic":"Artificial Intelligence",
  "article_limit":5,
  "language":"en"
}
```

Response

```json
{
  "request_id":"uuid",

  "topic":"Artificial Intelligence",

  "sources":[],

  "summary":"...",

  "transcript":{

    "host_a":"...",

    "host_b":"...",

    "full_script":"..."
  },

  "audio_url":"/static/audio/episode.mp3",

  "metadata":{}
}
```

---

# Environment Variables

Create:

```text
backend/.env
```

Add:

```env
GNEWS_API_KEY=your_api_key

GEMINI_API_KEY=your_api_key

EDGE_TTS_VOICE_A=en-US-AndrewNeural

EDGE_TTS_VOICE_B=en-US-EmmaNeural

AUDIO_BASE_URL=http://localhost:8000/static/audio
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/podcast-buddy.git

cd podcast-buddy
```

---

## Backend Setup

```bash
cd backend

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

Run:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

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

# UI Inspiration

Podcast Buddy draws inspiration from:

* Adobe Podcast
* Google NotebookLM Audio Overview
* Perplexity Discover
* Financial Times Editorial Design
* NPR Podcasts

---

# Future Improvements

* Multi-language podcasts
* Multiple voice options
* Background music
* Podcast history
* User authentication
* Spotify integration
* Cloud audio storage
* Podcast sharing links

---

# Current Status

### Backend

* News Retrieval : Complete
* AI Summary : Complete
* Dialogue Generation : Complete
* Edge TTS : Complete
* FFmpeg Audio Merge : Complete
* Static Audio Hosting : Complete

### Frontend

* Adobe Podcast Inspired UI : In Progress
* Waveform Player : Planned
* Episode Library : Planned

---

# Author

**Suman Dey**

B.Tech CSE Student
AI Engineer | Full Stack Developer | UI/UX Designer

---

# License

This project is licensed under the MIT License.
