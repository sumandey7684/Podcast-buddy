import { ArrowUpRight, CalendarDays, ShieldCheck } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Card, CardBody, CardHeader } from '@/components/ui/card'
import type { PodcastSource } from '@/types/podcast'

interface NewsSourcesProps {
  sources: PodcastSource[]
}

function formatPublishedDate(value: string): string {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return 'Recent'
  }

  return new Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(date)
}

function credibilityLabel(index: number): { label: string; tone: 'neutral' | 'accent' | 'success' | 'warning' } {
  if (index === 0) {
    return { label: 'Primary coverage', tone: 'accent' }
  }

  if (index < 3) {
    return { label: 'Supporting source', tone: 'success' }
  }

  return { label: 'Reference source', tone: 'neutral' }
}

export function NewsSources({ sources }: NewsSourcesProps) {
  return (
    <section id="sources" aria-labelledby="news-sources-heading" className="space-y-4">
      <div>
        <div className="section-label">News sources</div>
        <h2 id="news-sources-heading" className="section-title">
          Professional source ledger
        </h2>
        <p className="section-copy">
          Curated references used to build the episode, with publication details and direct article access.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {sources.map((source, index) => {
          const credibility = credibilityLabel(index)

          return (
            <Card key={`${source.url}-${index}`} className="group transition-all duration-200 hover:-translate-y-0.5 hover:border-white/14 hover:bg-surfaceAlt/95">
              <CardHeader className="space-y-3">
                <div className="flex items-center justify-between gap-4">
                  <Badge tone={credibility.tone}>
                    <ShieldCheck size={12} className="mr-1" />
                    {credibility.label}
                  </Badge>
                  <span className="flex items-center gap-1 text-xs text-white/38">
                    <CalendarDays size={12} />
                    {formatPublishedDate(source.published_at)}
                  </span>
                </div>

                <div className="space-y-2">
                  <h3 className="text-[15px] font-semibold leading-6 tracking-tight text-white">
                    {source.title}
                  </h3>
                  <p className="text-sm text-white/55">{source.snippet}</p>
                </div>
              </CardHeader>

              <CardBody className="flex items-center justify-between gap-4">
                <div>
                  <div className="text-xs font-semibold uppercase tracking-[0.2em] text-white/40">Publication</div>
                  <div className="mt-1 text-sm text-white/80">{source.source_name}</div>
                </div>

                <a
                  href={source.url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1 rounded-full border border-white/10 bg-white/5 px-3 py-2 text-sm text-white/80 transition-all duration-200 hover:border-white/18 hover:bg-white/10 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white/50"
                >
                  Open article
                  <ArrowUpRight size={14} />
                </a>
              </CardBody>
            </Card>
          )
        })}
      </div>
    </section>
  )
}