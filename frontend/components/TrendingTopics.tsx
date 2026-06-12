import { cn } from '@/lib/cn'

interface TrendingTopicsProps {
  topics: string[]
  onSelect: (topic: string) => void
  className?: string
  title?: string
}

export function TrendingTopics({ topics, onSelect, className, title = 'Trending topics' }: TrendingTopicsProps) {
  return (
    <section className={cn('space-y-3', className)} aria-labelledby="trending-topics-heading">
      <div className="flex items-center justify-between gap-3">
        <h3 id="trending-topics-heading" className="text-xs font-semibold uppercase tracking-[0.24em] text-white/45">
          {title}
        </h3>
        <span className="text-xs text-white/35">Updated live</span>
      </div>

      <div className="flex flex-wrap gap-2">
        {topics.map((topic) => (
          <button
            key={topic}
            type="button"
            onClick={() => onSelect(topic)}
            className="rounded-full border border-white/10 bg-white/4 px-3 py-2 text-sm text-white/80 transition-all duration-200 hover:border-white/18 hover:bg-white/8 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white/50"
          >
            {topic}
          </button>
        ))}
      </div>
    </section>
  )
}