"use client"

import { useEffect, useRef, useState } from 'react'
import { Download, Pause, Play, RotateCcw, Volume2 } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardBody, CardHeader } from '@/components/ui/card'

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000'

interface AudioPlayerProps {
  audioUrl: string
  title?: string
}

const playbackRates = [0.75, 1, 1.25, 1.5]

function formatTime(seconds: number): string {
  if (!Number.isFinite(seconds) || seconds < 0) {
    return '0:00'
  }

  const rounded = Math.floor(seconds)
  const minutes = Math.floor(rounded / 60)
  const remainingSeconds = rounded % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

function resolveAudioUrl(audioUrl: string): string {
  if (/^https?:\/\//i.test(audioUrl)) {
    return audioUrl
  }

  return `${apiBaseUrl.replace(/\/$/, '')}/${audioUrl.replace(/^\//, '')}`
}

export function AudioPlayer({ audioUrl, title = 'Podcast audio' }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [playbackRate, setPlaybackRate] = useState(1)
  const resolvedAudioUrl = resolveAudioUrl(audioUrl)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) {
      return
    }

    audio.playbackRate = playbackRate
  }, [playbackRate])

  useEffect(() => {
    const audio = audioRef.current

    return () => {
      if (audio) {
        audio.pause()
      }
    }
  }, [])

  const togglePlayback = async () => {
    const audio = audioRef.current
    if (!audio) {
      return
    }

    if (isPlaying) {
      audio.pause()
      setIsPlaying(false)
      return
    }

    await audio.play()
    setIsPlaying(true)
  }

  const handleSeek = (value: number) => {
    const audio = audioRef.current
    if (!audio || !Number.isFinite(value)) {
      return
    }

    audio.currentTime = value
    setCurrentTime(value)
  }

  return (
    <section id="audio" aria-labelledby="audio-heading" className="space-y-4">
      <div>
        <div className="section-label">Audio player</div>
        <h2 id="audio-heading" className="section-title">
          Premium playback
        </h2>
        <p className="section-copy">Custom controls, speed selection, progress tracking, and a clean download path for the final MP3.</p>
      </div>

      <Card>
        <CardHeader className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="text-xs font-semibold uppercase tracking-[0.24em] text-white/40">Now playing</div>
            <h3 className="mt-2 text-lg font-semibold tracking-tight text-white">{title}</h3>
          </div>
          <Badge tone="neutral">
            <Volume2 size={12} className="mr-1" />
            Studio mix
          </Badge>
        </CardHeader>

        <CardBody className="space-y-5">
          <audio
            ref={audioRef}
            src={resolvedAudioUrl}
            preload="metadata"
            onLoadedMetadata={(event) => setDuration(event.currentTarget.duration)}
            onTimeUpdate={(event) => setCurrentTime(event.currentTarget.currentTime)}
            onEnded={() => setIsPlaying(false)}
          />

          <div className="space-y-3 rounded-2xl border border-white/8 bg-white/[0.03] p-4">
            <div className="flex items-center justify-between gap-4 text-sm text-white/60">
              <span>{formatTime(currentTime)}</span>
              <span>{formatTime(duration)}</span>
            </div>

            <input
              type="range"
              min={0}
              max={duration || 0}
              step={0.1}
              value={currentTime}
              onChange={(event) => handleSeek(Number(event.target.value))}
              className="h-1.5 w-full cursor-pointer appearance-none rounded-full bg-white/10 accent-white"
              aria-label="Seek playback"
            />
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex flex-wrap gap-2">
              <Button onClick={togglePlayback} variant="primary" size="lg">
                {isPlaying ? <Pause size={14} /> : <Play size={14} />}
                {isPlaying ? 'Pause' : 'Play'}
              </Button>
              <Button
                onClick={() => {
                  const audio = audioRef.current
                  if (!audio) {
                    return
                  }
                  audio.currentTime = 0
                  audio.play().catch(() => undefined)
                  setIsPlaying(true)
                }}
                variant="secondary"
                size="lg"
              >
                <RotateCcw size={14} />
                Replay
              </Button>
            </div>

            <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 p-1">
              {playbackRates.map((rate) => (
                <button
                  key={rate}
                  type="button"
                  onClick={() => setPlaybackRate(rate)}
                  className={`min-w-12 rounded-full px-3 py-2 text-sm transition-all duration-200 ${
                    playbackRate === rate ? 'bg-white text-slate-950' : 'text-white/70 hover:bg-white/6 hover:text-white'
                  }`}
                >
                  {rate}x
                </button>
              ))}
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3 border-t border-white/8 pt-4">
            <a
              href={resolvedAudioUrl}
              download
              className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/78 transition-all duration-200 hover:border-white/18 hover:bg-white/8 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white/50"
            >
              <Download size={14} />
              Download MP3
            </a>
            <span className="text-sm text-white/40">Best experienced on headphones or speakers with a wide stereo image.</span>
          </div>
        </CardBody>
      </Card>
    </section>
  )
}