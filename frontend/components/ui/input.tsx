import { forwardRef } from 'react'

import { cn } from '@/lib/cn'

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input = forwardRef<HTMLInputElement, InputProps>(function Input({ className, ...props }, ref) {
  return (
    <input
      ref={ref}
      className={cn(
        'flex h-12 w-full rounded-full border border-white/10 bg-black/20 px-4 text-sm text-white placeholder:text-white/35 shadow-insetSoft transition-all duration-200 focus:border-white/20 focus:bg-black/30 focus:outline-none focus:ring-0',
        className,
      )}
      {...props}
    />
  )
})