"use client"

import { ArrowRight, Search } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Card, CardBody, CardHeader } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { TrendingTopics } from '@/components/TrendingTopics'

interface TopicInputProps {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
  onSelectTopic: (topic: string) => void
  onRecentSelect: (topic: string) => void
  trendingTopics: string[]
  recentSearches: string[]
  isLoading?: boolean
}

export function TopicInput({
  value,
  onChange,
  onSubmit,
  onSelectTopic,
  onRecentSelect,
  trendingTopics,
  recentSearches,
  isLoading = false,
}: TopicInputProps) {
  return (
    <Card>
      <CardHeader className="space-y-3">
        <div className="space-y-2">
          <div className="section-label">Topic generation</div>
          <h1 className="font-display text-3xl font-semibold tracking-tight text-white sm:text-4xl lg:text-[3.5rem] lg:leading-[1.04]">
            Turn any topic into a premium podcast briefing.
          </h1>
          <p className="section-copy max-w-4xl">
            Search the day&apos;s coverage, distill the noise, and generate a polished news-to-podcast episode in a single workflow.
          </p>
        </div>
      </CardHeader>

      <CardBody className="space-y-6">
        <form
          className="space-y-4"
          onSubmit={(event) => {
            event.preventDefault()
            onSubmit()
          }}
        >
          <label className="sr-only" htmlFor="topic-input">
            Enter a topic
          </label>
          <div className="relative">
            <Search className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-white/28" size={18} />
            <Input
              id="topic-input"
              name="topic"
              value={value}
              onChange={(event) => onChange(event.target.value)}
              placeholder="Try Artificial Intelligence, Tesla, or Cricket World Cup"
              autoComplete="off"
              aria-describedby="topic-input-help"
              className="h-14 pl-12 pr-36 text-[15px]"
            />
            <Button
              type="submit"
              variant="primary"
              size="md"
              disabled={isLoading || value.trim().length === 0}
              aria-label={isLoading ? 'Generating podcast' : 'Generate podcast'}
              className="absolute right-2 top-1/2 -translate-y-1/2"
            >
              {isLoading ? 'Generating…' : 'Generate podcast'}
              <ArrowRight size={14} />
            </Button>
          </div>
          <p id="topic-input-help" className="text-sm text-white/42">
            Focus on a company, market, event, or policy area. The result includes sources, summary, transcript, and audio.
          </p>
        </form>

        <TrendingTopics topics={trendingTopics} onSelect={onSelectTopic} />

        <section className="space-y-3" aria-labelledby="recent-searches-heading">
          <div className="flex items-center justify-between gap-3">
            <h3 id="recent-searches-heading" className="text-xs font-semibold uppercase tracking-[0.24em] text-white/45">
              Recent searches
            </h3>
            <span className="text-xs text-white/35">Local session</span>
          </div>

          <div className="flex flex-wrap gap-2">
            {recentSearches.length > 0 ? (
              recentSearches.map((item) => (
                <button
                  key={item}
                  type="button"
                  onClick={() => onRecentSelect(item)}
                  className="rounded-full border border-white/10 bg-white/4 px-3 py-2 text-sm text-white/75 transition-all duration-200 hover:border-white/18 hover:bg-white/8 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white/50"
                >
                  {item}
                </button>
              ))
            ) : (
              <p className="text-sm text-white/35">No recent searches yet. Generate a topic to populate this area.</p>
            )}
          </div>
        </section>
      </CardBody>
    </Card>
  )
}