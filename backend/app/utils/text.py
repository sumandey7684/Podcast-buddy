import re


def clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def merge_context(parts: list[str]) -> str:
    cleaned_parts = [clean_text(part) for part in parts if part and part.strip()]
    return "\n".join(cleaned_parts)