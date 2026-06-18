import type { EditorialSummary } from '@/types/summary'
import type { PodcastGenerationResponse } from '@/types/podcast'

function truncate(value: string, length: number): string {
  if (value.length <= length) {
    return value
  }

  return `${value.slice(0, length).trim()}...`
}

function sentenceSplit(value: string): string[] {
  return value
    .split(/\.(?=\s|$)/)
    .map((item) => item.trim())
    .filter(Boolean)
}

export function buildEditorialSummary(result: PodcastGenerationResponse): EditorialSummary {
  let parsed: Record<string, string[]> = {}
  try {
    parsed = JSON.parse(result.summary) as Record<string, string[]>
  } catch {
    parsed = {}
  }

  const mainEvents: string[] = Array.isArray(parsed.main_events) ? parsed.main_events : []
  const keyFacts: string[] = Array.isArray(parsed.key_facts) ? parsed.key_facts : []
  const futureImplications: string[] = Array.isArray(parsed.future_implications) ? parsed.future_implications : []
  const expertOpinions: string[] = Array.isArray(parsed.expert_opinions) ? parsed.expert_opinions : []
  const takeaways = result.sources.slice(0, 3).map((source) => truncate(source.title, 96))
  const developments = result.sources.slice(0, 3).map((source) => truncate(source.snippet, 112))
  const lead =
    mainEvents.length > 0
      ? mainEvents[0]
      : `Coverage spans ${result.sources.length} sources on ${result.topic}.`

  const futureImplicationItems =
    futureImplications.length > 0
      ? futureImplications.slice(0, 3)
      : [truncate(`The story is still evolving across ${result.sources.length} reported sources.`, 112)]

  const expertOpinionItems =
    expertOpinions.length > 0
      ? expertOpinions.slice(0, 3)
      : [`Coverage spans ${result.metadata.article_count} articles from ${result.metadata.provider_name}.`]

  return {
    lead,
    sections: [
      {
        title: 'Key takeaways',
        items: takeaways.length > 0 ? takeaways : [truncate(result.summary, 96)],
      },
      {
        title: 'Important developments',
        items: developments.length > 0 ? developments : [truncate(result.summary, 112)],
      },
      {
        title: 'Future implications',
        items: futureImplicationItems,
      },
      {
        title: 'Expert opinions',
        items: expertOpinionItems,
      },
    ],
  }
}