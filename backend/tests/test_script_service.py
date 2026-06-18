from __future__ import annotations

import pytest

from app.services.script_service import ScriptService


def full_script_lines(full_script: str) -> list[str]:
    return [line for line in full_script.splitlines() if line.strip()]


@pytest.mark.asyncio
async def test_generate_dialogue_returns_alternating_minimum_six_turns() -> None:
    result = await ScriptService().generate_dialogue(
        topic="AI infrastructure",
        summary={
            "main_events": ["major cloud vendors expanded AI capacity"],
            "key_facts": ["chip demand is rising"],
            "future_implications": ["data center investment may accelerate"],
            "expert_opinions": ["analysts expect supply constraints"],
        },
    )

    assert len(result) >= 6
    assert [turn["speaker"] for turn in result[:6]] == [
        "HOST_A",
        "HOST_B",
        "HOST_A",
        "HOST_B",
        "HOST_A",
        "HOST_B",
    ]
    assert all(turn["text"] for turn in result)


@pytest.mark.asyncio
async def test_generate_dialogue_handles_empty_summary_without_none_values() -> None:
    result = await ScriptService().generate_dialogue(topic="", summary={})

    assert result
    assert all(turn["speaker"] for turn in result)
    assert all(turn["text"] for turn in result)
