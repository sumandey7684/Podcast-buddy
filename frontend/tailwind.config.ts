import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './lib/**/*.{ts,tsx}',
    './types/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: 'var(--color-bg)',
        surface: 'var(--color-surface)',
        surfaceAlt: 'var(--color-surface-alt)',
        line: 'var(--color-line)',
        text: 'var(--color-text)',
        muted: 'var(--color-muted)',
        accent: 'var(--color-accent)',
        accentSoft: 'var(--color-accent-soft)',
      },
      boxShadow: {
        soft: '0 18px 48px rgba(0, 0, 0, 0.24)',
        insetSoft: 'inset 0 1px 0 rgba(255, 255, 255, 0.04)',
      },
      borderRadius: {
        '2xl': '1.25rem',
      },
      fontFamily: {
        sans: ['var(--font-manrope)', 'sans-serif'],
        display: ['var(--font-space-grotesk)', 'sans-serif'],
      },
      gridTemplateColumns: {
        shell: 'minmax(0, 1.6fr) minmax(320px, 0.9fr)',
      },
    },
  },
  plugins: [],
}

export default config