import axios from 'axios'

import type { PodcastGenerationRequest, PodcastGenerationResponse } from '@/types/podcast'

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000'

const api = axios.create({
  baseURL: apiBaseUrl,
  timeout: 45000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export function getApiBaseUrl(): string {
  return apiBaseUrl
}

export async function generatePodcast(topic: string): Promise<PodcastGenerationResponse> {
  const payload: PodcastGenerationRequest = {
    topic,
    article_limit: 10,
    language: 'en',
  }

  const { data } = await api.post<PodcastGenerationResponse>('/api/v1/podcast/generate', payload)
  return data
}

export function formatApiError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const responseMessage = error.response?.data?.detail
    if (typeof responseMessage === 'string') {
      return responseMessage
    }

    if (Array.isArray(responseMessage)) {
      return responseMessage.join(', ')
    }

    return error.message || 'Unable to reach the Podcast Buddy API.'
  }

  if (error instanceof Error) {
    return error.message
  }

  return 'Something went wrong while generating the podcast.'
}