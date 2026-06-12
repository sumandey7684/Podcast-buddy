export interface StructuredSummary {
  main_events: string[]
  key_facts: string[]
  future_implications: string[]
  expert_opinions: string[]
}

export interface SummarySection {
  title: string
  items: string[]
}

export interface EditorialSummary {
  lead: string
  sections: SummarySection[]
}