import { Sparkles, Radio } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

export function Navbar() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/6 bg-[#090a0c]/85 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/6 text-white shadow-insetSoft">
            <Radio size={16} strokeWidth={2.2} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-display text-sm font-semibold tracking-[0.18em] text-white uppercase">Podcast Buddy</span>
              <Badge tone="neutral">Live</Badge>
            </div>
            <p className="text-xs text-white/45">News into a polished podcast briefing</p>
          </div>
        </div>

        <nav className="hidden items-center gap-2 md:flex" aria-label="Primary navigation">
          <Button variant="ghost" size="sm" className="text-white/70 hover:text-white">
            Sources
          </Button>
          <Button variant="ghost" size="sm" className="text-white/70 hover:text-white">
            Transcript
          </Button>
          <Button variant="ghost" size="sm" className="text-white/70 hover:text-white">
            Audio
          </Button>
          <Button variant="secondary" size="sm">
            <Sparkles size={14} />
            Product ready
          </Button>
        </nav>
      </div>
    </header>
  )
}