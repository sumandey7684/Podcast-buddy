import { Card, CardBody, CardHeader } from '@/components/ui/card'

const loadingSteps = [
  'Collecting recent headlines',
  'Cleaning source material',
  'Writing the editorial summary',
  'Building the two-host conversation',
  'Preparing audio delivery',
]

interface LoadingStateProps {
  topic: string
  stepIndex: number
}

export function LoadingState({ topic, stepIndex }: LoadingStateProps) {
  const activeStep = loadingSteps[Math.min(stepIndex, loadingSteps.length - 1)]

  return (
    <section aria-live="polite" aria-busy="true" className="space-y-4">
      <Card>
        <CardHeader className="space-y-2">
          <div className="section-label">Processing</div>
          <h2 className="section-title">Building your podcast briefing for {topic}.</h2>
          <p className="section-copy">
            The system is pulling in fresh coverage, compressing the context, and shaping a studio-style conversation.
          </p>
        </CardHeader>

        <CardBody className="space-y-6">
          <div className="rounded-2xl border border-white/8 bg-black/20 p-4">
            <div className="flex items-center justify-between gap-4 text-sm">
              <span className="text-white/72">{activeStep}</span>
              <span className="font-medium text-white/60">Step {Math.min(stepIndex + 1, loadingSteps.length)} of {loadingSteps.length}</span>
            </div>
            <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-white/6">
              <div
                className="h-full rounded-full bg-white transition-all duration-500 ease-out"
                style={{ width: `${Math.min(100, ((stepIndex + 1) / loadingSteps.length) * 100)}%` }}
              />
            </div>
          </div>

          <div className="grid gap-4 lg:grid-cols-3">
            {[1, 2, 3].map((item) => (
              <div key={item} className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
                <div className="space-y-3">
                  <div className="h-3 w-28 rounded-full bg-white/8" />
                  <div className="h-4 w-2/3 rounded-full bg-white/8" />
                  <div className="h-4 w-5/6 rounded-full bg-white/6" />
                  <div className="h-4 w-1/2 rounded-full bg-white/6" />
                </div>
              </div>
            ))}
          </div>
        </CardBody>
      </Card>
    </section>
  )
}