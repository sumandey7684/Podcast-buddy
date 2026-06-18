"use client"

import { useState } from 'react'
import { ChevronRight, FileText, Mic2 } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Card, CardBody, CardHeader } from '@/components/ui/card'
import type { PodcastTranscript } from '@/types/podcast'

interface TranscriptViewerProps {
  transcript: PodcastTranscript
}

type TranscriptSection = 'overview' | 'host_a' | 'host_b' | 'full'

export function TranscriptViewer({ transcript }: TranscriptViewerProps) {
  const [activeSection, setActiveSection] = useState<TranscriptSection>('overview')

  const hostALines = transcript.host_a.split(/\n+/).filter(Boolean)
  const hostBLines = transcript.host_b.split(/\n+/).filter(Boolean)
  const fullLines = transcript.full_script.split(/\n+/).filter(Boolean)

  const jumpTo = (section: TranscriptSection) => {
    setActiveSection(section)
    const element = document.getElementById(`transcript-${section}`)
    element?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  return (
    <section id="transcript" aria-labelledby="transcript-heading" className="space-y-4">
      <div>
        <div className="section-label">Podcast transcript</div>
        <h2 id="transcript-heading" className="section-title">
          Two-host conversation reader
        </h2>
        <p className="section-copy">
          A transcript-first experience with sticky navigation and an editorial reading flow instead of chat-style bubbles.
        </p>
      </div>

      <Card>
        <CardHeader className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Badge tone="neutral">
              <Mic2 size={12} className="mr-1" />
              Studio transcript
            </Badge>
            <span className="text-xs text-white/35">Swipe or scroll to navigate</span>
          </div>

          <nav aria-label="Transcript sections" className="flex flex-wrap gap-2">
            {[
              { key: 'overview', label: 'Overview' },
              { key: 'host_a', label: 'HOST_A' },
              { key: 'host_b', label: 'HOST_B' },
              { key: 'full', label: 'Full transcript' },
            ].map((item) => (
              <button
                key={item.key}
                type="button"
                onClick={() => jumpTo(item.key as TranscriptSection)}
                className={`inline-flex items-center gap-1 rounded-full border px-3 py-2 text-sm transition-all duration-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white/50 ${
                  activeSection === item.key
                    ? 'border-white/18 bg-white text-slate-950'
                    : 'border-white/10 bg-white/5 text-white/75 hover:border-white/18 hover:bg-white/8 hover:text-white'
                }`}
              >
                {item.label}
                <ChevronRight size={13} />
              </button>
            ))}
          </nav>
        </CardHeader>

        <CardBody>
          <div className="grid gap-4 lg:grid-cols-[240px_minmax(0,1fr)]">
            <aside className="space-y-3 lg:sticky lg:top-24 lg:self-start">
              <div className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
                <div className="text-xs font-semibold uppercase tracking-[0.24em] text-white/40">Narrative structure</div>
                <div className="mt-4 space-y-3 text-sm text-white/70">
                  <div className="flex items-center justify-between gap-3">
                    <span>HOST_A</span>
                    <span className="text-white/38">Lead framing</span>
                  </div>
                  <div className="flex items-center justify-between gap-3">
                    <span>HOST_B</span>
                    <span className="text-white/38">Follow-up angle</span>
                  </div>
                  <div className="flex items-center justify-between gap-3">
                    <span>Dialogue</span>
                    <span className="text-white/38">Full read</span>
                  </div>
                </div>
              </div>

              <div className="rounded-2xl border border-white/8 bg-white/[0.03] p-4 text-sm text-white/60">
                <div className="flex items-center gap-2 text-white/80">
                  <FileText size={16} />
                  Reading experience
                </div>
                <p className="mt-3 leading-6">
                  The layout is intentionally editorial: clear speaker blocks, generous spacing, and a stable reading rhythm for longer conversations.
                </p>
              </div>
            </aside>

            <div className="space-y-4">
              <article id="transcript-overview" className="rounded-2xl border border-white/8 bg-black/20 p-5">
                <div className="text-xs font-semibold uppercase tracking-[0.24em] text-white/40">Overview</div>
                <h3 className="mt-2 text-lg font-semibold tracking-tight text-white">Conversation framing</h3>
                <p className="mt-3 max-w-3xl text-sm leading-7 text-white/72">
                  HOST_A sets up the news cycle with the main storyline, while HOST_B reacts, contextualizes, and pushes deeper on the implications. The result reads like a polished broadcast briefing.
                </p>
              </article>

              <article id="transcript-host_a" className="rounded-2xl border border-white/8 bg-white/[0.03] p-5">
                <div className="flex items-center justify-between gap-4">
                  <Badge tone="neutral">HOST_A</Badge>
                  <span className="text-xs text-white/35">{hostALines.length} lines</span>
                </div>
                <div className="mt-4 space-y-3 text-[15px] leading-7 text-white/82">
                  {hostALines.map((line, lineIndex) => (
                    <p key={`host-a-${lineIndex}`} className="border-l border-white/10 pl-4">
                      {line}
                    </p>
                  ))}
                </div>
              </article>

              <article id="transcript-host_b" className="rounded-2xl border border-white/8 bg-white/[0.03] p-5">
                <div className="flex items-center justify-between gap-4">
                  <Badge tone="neutral">HOST_B</Badge>
                  <span className="text-xs text-white/35">{hostBLines.length} lines</span>
                </div>
                <div className="mt-4 space-y-3 text-[15px] leading-7 text-white/82">
                  {hostBLines.map((line, lineIndex) => (
                    <p key={`host-b-${lineIndex}`} className="border-l border-white/10 pl-4">
                      {line}
                    </p>
                  ))}
                </div>
              </article>

              <article id="transcript-full" className="rounded-2xl border border-white/8 bg-black/20 p-5">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <div className="text-xs font-semibold uppercase tracking-[0.24em] text-white/40">Full transcript</div>
                    <h3 className="mt-2 text-lg font-semibold tracking-tight text-white">Complete episode readout</h3>
                  </div>
                  <Badge tone="accent">Ready for TTS</Badge>
                </div>
                <div className="mt-4 max-h-[32rem] space-y-3 overflow-y-auto pr-2 text-[15px] leading-7 text-white/80">
                  {fullLines.map((line, lineIndex) => (
                    <div key={`full-${lineIndex}`} className="rounded-2xl border border-white/8 bg-white/[0.03] px-4 py-3">
                      {line}
                    </div>
                  ))}
                </div>
              </article>
            </div>
          </div>
        </CardBody>
      </Card>
    </section>
  )
}