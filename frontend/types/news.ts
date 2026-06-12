export interface NewsArticle {
  title: string
  description: string | null
  source: string
  url: string
  published_at: string | null
}

export interface NewsSearchRequest {
  topic: string
  limit: number
  language: string
}

export interface NewsSearchResponse {
  topic: string
  total_results: number
  articles: NewsArticle[]
}