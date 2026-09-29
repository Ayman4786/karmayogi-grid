from ai.skill_extraction.extractor import extract_skill_phrases


def test_extract_skill_phrases():
    text = (
        "I understand sampling terminology. "
        "I can select an appropriate sampling method."
    )

    phrases = extract_skill_phrases(text)

    assert len(phrases) >= 2
    assert any("sampling" in phrase.lower() for phrase in phrases)


def test_empty_text():
    assert extract_skill_phrases("") == []
    assert extract_skill_phrases("   ") == []