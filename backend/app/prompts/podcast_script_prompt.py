from __future__ import annotations

import json
from typing import Any


def build_podcast_script_prompt(
    structured_summary: dict[str, list[str]],
    topic: str | None = None,
    conversation_minutes: int = 6,
) -> str:
    payload = json.dumps(structured_summary, ensure_ascii=False, indent=2)
    topic_context = f"Topic: {topic}\n" if topic else ""

    return (
        "You are a senior podcast writer for Podcast Buddy. "
        "Write a natural, human-sounding conversation between HOST_A and HOST_B. "
        "The conversation must be conversational, warm, and informative, with follow-up questions, "
        "natural reactions, short interruptions, and flowing back-and-forth dialogue. "
        "Avoid robotic phrasing, repeated sentence patterns, and lecture-style narration. "
        "Target a 5-7 minute conversation. "
        "Use clear speaker labels exactly as HOST_A and HOST_B. "
        "Return ONLY valid JSON with exactly these keys: host_a, host_b, full_script, estimated_duration_minutes. "
        "The host_a and host_b fields should contain the speaking lines for each host, while full_script "
        "should contain the complete dialogue with speaker labels and line breaks. "
        "Do not include markdown fences, notes, or extra keys.\n\n"
        f"{topic_context}"
        f"Desired duration: {conversation_minutes} minutes\n\n"
        f"Structured summary:\n{payload}"
    )
