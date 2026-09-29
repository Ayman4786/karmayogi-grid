from ai.skill_extraction.dictionary import load_competency_dictionary


def test_dictionary_loads():
    dictionary = load_competency_dictionary()

    assert len(dictionary) > 0


def test_sampling_is_in_dictionary():
    dictionary = load_competency_dictionary()

    competency_ids = {
        item["competency_id"]
        for item in dictionary
    }

    assert "STAT.SAMPLING" in competency_ids