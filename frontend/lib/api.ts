import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios'

import type { PodcastGenerationRequest, PodcastGenerationResponse } from '@/types/podcast'

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000'
const requestTimeoutMs = 120000
const maxNetworkRetries = 2

const api = axios.create({
  baseURL: apiBaseUrl,
  timeout: requestTimeoutMs,
  headers: {
    'Content-Type': 'application/json',
  },
})

interface RetryableRequestConfig extends InternalAxiosRequestConfig {
  retryCount?: number
}

function isRetryableNetworkFailure(error: AxiosError): boolean {
  return !error.response && (error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK' || error.code === 'ETIMEDOUT')
}

api.interceptors.request.use((config) => {
  config.headers.set('X-Podcast-Buddy-Client', 'nextjs')
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const config = error.config as RetryableRequestConfig | undefined
    if (!config || !isRetryableNetworkFailure(error)) {
      return Promise.reject(error)
    }

    config.retryCount = config.retryCount ?? 0
    if (config.retryCount >= maxNetworkRetries) {
      return Promise.reject(error)
    }

    const retryCount = config.retryCount + 1
    config.retryCount = retryCount
    await new Promise((resolve) => globalThis.setTimeout(resolve, 600 * retryCount))
    return api(config)
  },
)

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
    if (error.code === 'ECONNABORTED' || error.code === 'ETIMEDOUT') {
      return 'Podcast generation is taking longer than expected. Please retry in a moment.'
    }

    if (!error.response) {
      return 'Unable to reach the Podcast Buddy API. Check that the backend is running.'
    }

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