"""
Skill phrase extraction.

This module extracts candidate competency-related phrases from
learner text before semantic matching.
"""

import re


def extract_skill_phrases(text: str) -> list[str]:
    """
    Extract candidate skill phrases from text.

    This is intentionally lightweight. Semantic matching is handled
    separately by matcher.py.
    """

    if not text or not text.strip():
        return []

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text.strip())

    # Split into sentences / clauses
    parts = re.split(r"[.!?,;:\n]+", text)

    phrases = []

    for part in parts:
        phrase = part.strip()

        if phrase and len(phrase.split()) >= 2:
            phrases.append(phrase)

    return phrases