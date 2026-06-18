from __future__ import annotations

import re
from collections.abc import Mapping, Sequence


SummaryPayload = Mapping[str, Sequence[object]]


class ScriptServiceError(Exception):
    pass


class ScriptService:
    async def generate_dialogue(self, topic: str, summary: SummaryPayload) -> list[dict[str, str]]:
        topic_text = self._clean_text(topic) or "this story"
        summary_values = self._normalize_summary(summary)

        main_event = self._pick(summary_values["main_events"], "the latest reporting is still developing")
        key_fact = self._pick(summary_values["key_facts"], "the clearest details are still coming into focus")
        future_implication = self._pick(
            summary_values["future_implications"],
            "the next updates will help show how this affects people and organizations",
        )
        expert_opinion = self._pick(
            summary_values["expert_opinions"],
            "analysts are watching for stronger signals before drawing firm conclusions",
        )

        turns = [
            (
                "HOST_A",
                f"Welcome to Podcast Buddy. Today we are looking at {topic_text}, and the headline is that {main_event}.",
            ),
            (
                "HOST_B",
                f"That is a useful starting point, because it gives us one clear thread to follow without overloading the listener.",
            ),
            (
                "HOST_A",
                f"One important fact here is that {key_fact}.",
            ),
            (
                "HOST_B",
                f"What stands out to me is this perspective: {expert_opinion}.",
            ),
            (
                "HOST_A",
                f"Looking ahead, the big implication is that {future_implication}.",
            ),
            (
                "HOST_B",
                f"So the takeaway is simple: keep an eye on {topic_text}, because the story is moving and the context matters.",
            ),
        ]

        full_script = "\n".join(f"{speaker}: {text}" for speaker, text in turns)
        host_a = " ".join(text for speaker, text in turns if speaker == "HOST_A")
        host_b = " ".join(text for speaker, text in turns if speaker == "HOST_B")

        return [{"speaker": speaker, "text": text} for speaker, text in turns]

    @staticmethod
    def _normalize_summary(summary: SummaryPayload) -> dict[str, list[str]]:
        return {
            "main_events": ScriptService._clean_items(summary.get("main_events", [])),
            "key_facts": ScriptService._clean_items(summary.get("key_facts", [])),
            "future_implications": ScriptService._clean_items(summary.get("future_implications", [])),
            "expert_opinions": ScriptService._clean_items(summary.get("expert_opinions", [])),
        }

    @staticmethod
    def _clean_items(items: Sequence[object]) -> list[str]:
        return [cleaned for item in items if (cleaned := ScriptService._clean_text(str(item)))]

    @staticmethod
    def _pick(items: Sequence[str], fallback: str) -> str:
        if not items:
            return fallback
        return items[0]

    @staticmethod
    def _clean_text(value: str) -> str:
        return re.sub(r"\s+", " ", value).strip()
