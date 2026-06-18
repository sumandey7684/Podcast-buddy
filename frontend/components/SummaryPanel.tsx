import { ArrowRight, Lightbulb } from 'lucide-react'

import { Card, CardBody, CardHeader } from '@/components/ui/card'
import type { EditorialSummary } from '@/types/summary'

interface SummaryPanelProps {
  topic: string
  summary: EditorialSummary
}

export function SummaryPanel({ topic, summary }: SummaryPanelProps) {
  return (
    <section id="summary" aria-labelledby="summary-heading" className="space-y-4">
      <div>
        <div className="section-label">AI summary</div>
        <h2 id="summary-heading" className="section-title">
          Editorial summary for {topic}
        </h2>
        <p className="section-copy">
          The strongest signals from the reported coverage, organized into a newsroom-style briefing.
        </p>
      </div>

      <Card>
        <CardHeader className="space-y-4">
          <div className="flex items-start gap-4">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-white/80">
              <Lightbulb size={18} />
            </div>
            <div className="space-y-2">
              <div className="text-xs font-semibold uppercase tracking-[0.24em] text-white/40">Lead summary</div>
              <p className="text-[15px] leading-7 text-white/82">{summary.lead}</p>
            </div>
          </div>
        </CardHeader>

        <CardBody>
          <div className="grid gap-4 lg:grid-cols-2">
            {summary.sections.map((section) => (
              <div key={section.title} className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
                <div className="flex items-center justify-between gap-4">
                  <h3 className="text-sm font-semibold tracking-tight text-white">{section.title}</h3>
                  <ArrowRight size={14} className="text-white/28" />
                </div>

                <ul className="mt-4 space-y-3">
                  {section.items.map((item, itemIndex) => (
                    <li key={`${section.title}-${itemIndex}`} className="flex gap-3 text-sm leading-6 text-white/70">
                      <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-white/35" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </CardBody>
      </Card>
    </section>
  )
}