import type { StructuredSummary } from './summary'

export interface PodcastSource {
  title: string
  source_name: string
  url: string
  published_at: string
  snippet: string
}

export interface PodcastTranscript {
  host_a: string
  host_b: string
  full_script: string
}

export interface PodcastMetadata {
  article_count: number
  generated_at: string
  provider_name: string
}

export interface PodcastGenerationRequest {
  topic: string
  article_limit: number
  language: string
}

export interface PodcastGenerationResponse {
  request_id: string
  topic: string
  sources: PodcastSource[]
  summary: string
  transcript: PodcastTranscript
  audio_url: string
  metadata: PodcastMetadata
  structured_summary?: StructuredSummary | null
}