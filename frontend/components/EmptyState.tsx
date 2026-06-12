import { ArrowUpRight, PlayCircle, Radio } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Card, CardBody } from '@/components/ui/card'

interface EmptyStateProps {
  onTryExample: (topic: string) => void
  examples: string[]
}

export function EmptyState({ onTryExample, examples }: EmptyStateProps) {
  return (
    <section aria-labelledby="empty-state-heading" className="space-y-4">
      <Card>
        <CardBody className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr] lg:items-center">
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-white/70">
              <Radio size={16} />
              <span className="text-xs font-semibold uppercase tracking-[0.24em] text-white/40">Onboarding</span>
            </div>
            <div>
              <h2 id="empty-state-heading" className="font-display text-2xl font-semibold tracking-tight text-white sm:text-3xl">
                Start with a topic and the newsroom comes alive.
              </h2>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-white/60 sm:text-[15px]">
                Enter a subject like a market, company, tournament, or policy issue. Podcast Buddy will gather coverage, write the summary, build the transcript, and prepare the audio.
              </p>
            </div>

            <div className="flex flex-wrap gap-3">
              {examples.map((topic) => (
                <Button key={topic} variant="secondary" size="md" onClick={() => onTryExample(topic)}>
                  <PlayCircle size={14} />
                  {topic}
                </Button>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-white/8 bg-white/[0.03] p-5">
            <div className="text-xs font-semibold uppercase tracking-[0.24em] text-white/40">What you’ll get</div>
            <ul className="mt-4 space-y-3 text-sm leading-6 text-white/70">
              <li className="flex gap-3"><span className="mt-2 h-1.5 w-1.5 rounded-full bg-white/40" />News sources with dates and references</li>
              <li className="flex gap-3"><span className="mt-2 h-1.5 w-1.5 rounded-full bg-white/40" />Editorial AI summary for quick scanning</li>
              <li className="flex gap-3"><span className="mt-2 h-1.5 w-1.5 rounded-full bg-white/40" />HOST_A and HOST_B podcast transcript</li>
              <li className="flex gap-3"><span className="mt-2 h-1.5 w-1.5 rounded-full bg-white/40" />A downloadable MP3 with premium controls</li>
            </ul>

            <a
              href="#"
              onClick={(event) => event.preventDefault()}
              className="mt-5 inline-flex items-center gap-2 text-sm font-medium text-white/78 transition-colors hover:text-white"
            >
              Read the full workflow
              <ArrowUpRight size={14} />
            </a>
          </div>
        </CardBody>
      </Card>
    </section>
  )
}