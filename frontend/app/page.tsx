"use client"

import { useEffect, useState } from 'react'

import { AudioPlayer } from '@/components/AudioPlayer'
import { EmptyState } from '@/components/EmptyState'
import { ErrorState } from '@/components/ErrorState'
import { LoadingState } from '@/components/LoadingState'
import { Navbar } from '@/components/Navbar'
import { NewsSources } from '@/components/NewsSources'
import { SummaryPanel } from '@/components/SummaryPanel'
import { TopicInput } from '@/components/TopicInput'
import { TranscriptViewer } from '@/components/TranscriptViewer'
import { generatePodcast, formatApiError } from '@/lib/api'
import { buildEditorialSummary } from '@/lib/summary'
import type { PodcastGenerationResponse } from '@/types/podcast'

const trendingTopics = ['Artificial Intelligence', 'Tesla', 'Cricket World Cup', 'Fed rate cuts', 'OpenAI']
const onboardingExamples = ['Artificial Intelligence', 'Tesla', 'Cricket World Cup']
const loadingStages = ['Collecting sources', 'Cleaning articles', 'Writing summary', 'Generating transcript', 'Preparing audio']

export default function HomePage() {
  const [topic, setTopic] = useState('Artificial Intelligence')
  const [currentTopic, setCurrentTopic] = useState('')
  const [result, setResult] = useState<PodcastGenerationResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [stageIndex, setStageIndex] = useState(0)
  const [recentSearches, setRecentSearches] = useState<string[]>([])

  useEffect(() => {
    const savedSearches = window.localStorage.getItem('podcast-buddy:recent-searches')
    if (!savedSearches) {
      return
    }

    try {
      const parsed = JSON.parse(savedSearches)
      if (Array.isArray(parsed)) {
        setRecentSearches(parsed.filter((item): item is string => typeof item === 'string'))
      }
    } catch {
      window.localStorage.removeItem('podcast-buddy:recent-searches')
    }
  }, [])

  useEffect(() => {
    if (!isLoading) {
      return
    }

    const timer = window.setInterval(() => {
      setStageIndex((value) => (value + 1) % loadingStages.length)
    }, 850)

    return () => window.clearInterval(timer)
  }, [isLoading])

  const persistRecentSearches = (value: string) => {
    setRecentSearches((existing) => {
      const next = [value, ...existing.filter((item) => item.toLowerCase() !== value.toLowerCase())].slice(0, 5)
      window.localStorage.setItem('podcast-buddy:recent-searches', JSON.stringify(next))
      return next
    })
  }

  const handleGenerate = async (value = topic) => {
    const normalizedTopic = value.trim()
    if (!normalizedTopic) {
      return
    }

    setIsLoading(true)
    setError(null)
    setCurrentTopic(normalizedTopic)
    setStageIndex(0)

    try {
      const response = await generatePodcast(normalizedTopic)
      setResult(response)
      setTopic(normalizedTopic)
      persistRecentSearches(normalizedTopic)
    } catch (requestError) {
      setError(formatApiError(requestError))
      setResult(null)
    } finally {
      setIsLoading(false)
    }
  }

  const summary = result ? buildEditorialSummary(result) : null

  return (
    <div className="relative min-h-screen overflow-x-hidden">
      <Navbar />

      <main className="mx-auto max-w-7xl px-4 pb-16 pt-24 sm:px-6 lg:px-8">
        <div className="space-y-8">
          <TopicInput
            value={topic}
            onChange={setTopic}
            onSubmit={() => handleGenerate(topic)}
            onSelectTopic={(value) => setTopic(value)}
            onRecentSelect={(value) => {
              setTopic(value)
              handleGenerate(value)
            }}
            trendingTopics={trendingTopics}
            recentSearches={recentSearches}
            isLoading={isLoading}
          />

          {error ? <ErrorState message={error} onRetry={() => handleGenerate(currentTopic || topic)} /> : null}

          {isLoading ? <LoadingState topic={currentTopic || topic} stepIndex={stageIndex} /> : null}

          {!isLoading && !error && !result ? (
            <EmptyState
              onTryExample={(value) => {
                setTopic(value)
                handleGenerate(value)
              }}
              examples={onboardingExamples}
            />
          ) : null}

          {!isLoading && !error && result && summary ? (
            <div className="space-y-10">
              <div className="grid gap-8 xl:grid-cols-[minmax(0,1.1fr)_minmax(340px,0.9fr)]">
                <SummaryPanel topic={result.topic} summary={summary} />
                <AudioPlayer audioUrl={result.audio_url} title={`${result.topic} podcast briefing`} />
              </div>

              <NewsSources sources={result.sources} />

              <TranscriptViewer transcript={result.transcript} />
            </div>
          ) : null}
        </div>
      </main>
    </div>
  )
}