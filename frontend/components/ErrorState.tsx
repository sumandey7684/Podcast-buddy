import { AlertTriangle, RotateCcw } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Card, CardBody } from '@/components/ui/card'

interface ErrorStateProps {
  message: string
  onRetry: () => void
}

export function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <section aria-labelledby="error-state-heading">
      <Card>
        <CardBody className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="flex items-start gap-4">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-red-400/20 bg-red-400/10 text-red-200">
              <AlertTriangle size={18} />
            </div>
            <div>
              <h2 id="error-state-heading" className="text-lg font-semibold tracking-tight text-white">
                Generation failed
              </h2>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-white/62">{message}</p>
            </div>
          </div>

          <Button variant="secondary" size="lg" onClick={onRetry}>
            <RotateCcw size={14} />
            Retry
          </Button>
        </CardBody>
      </Card>
    </section>
  )
}