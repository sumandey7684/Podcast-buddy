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
  const takeaways = result.sources.slice(0, 3).map((source) => truncate(source.title, 96))
  const developments = result.sources.slice(0, 3).map((source) => truncate(source.snippet, 112))
  const implications = sentenceSplit(result.summary).slice(0, 3)

  const fallbackImplication =
    implications.length > 0
      ? implications
      : [truncate(`The story is still evolving across ${result.sources.length} reported sources.`, 112)]

  return {
    lead: result.summary,
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
        items: fallbackImplication,
      },
      {
        title: 'Expert opinions',
        items: result.sources.length > 0 ? [`Coverage spans ${result.metadata.article_count} articles from ${result.metadata.provider_name}.`] : [],
      },
    ],
  }
}