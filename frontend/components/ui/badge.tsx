import { cn } from '@/lib/cn'

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  tone?: 'neutral' | 'accent' | 'success' | 'warning'
}

const toneClasses: Record<NonNullable<BadgeProps['tone']>, string> = {
  neutral: 'bg-white/6 text-white border-white/10',
  accent: 'bg-white text-slate-950 border-white',
  success: 'bg-emerald-400/10 text-emerald-300 border-emerald-400/20',
  warning: 'bg-amber-400/10 text-amber-300 border-amber-400/20',
}

export function Badge({ className, tone = 'neutral', ...props }: BadgeProps) {
  return <span className={cn('inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium', toneClasses[tone], className)} {...props} />
}