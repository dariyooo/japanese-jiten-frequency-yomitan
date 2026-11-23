import json
import zipfile

import pytest

from japanese_jiten_frequency.build import DICTIONARIES, build_dictionary_index, read_banks


@pytest.mark.parametrize("dictionary", DICTIONARIES, ids=lambda d: d.variant)
def test_index_has_required_fields(dictionary):
    index = build_dictionary_index(dictionary)
    for field in ("title", "author", "url", "description", "attribution", "sourceLanguage"):
        assert index[field]
    assert index["frequencyMode"] == "rank-based"
    assert index["downloadUrl"].endswith(f"japanese-jiten-frequency-yomitan-{dictionary.variant}.zip")


def _archive(tmp_path, files: dict, mode: str = "rank-based"):
    archive = tmp_path / "jiten.zip"
    with zipfile.ZipFile(archive, "w") as zipf:
        zipf.writestr("index.json", json.dumps({"title": "Jiten", "frequencyMode": mode}))
        for name, entries in files.items():
            zipf.writestr(name, json.dumps(entries, ensure_ascii=False))
    return archive


def test_reads_banks_in_numeric_order(tmp_path):
    archive = _archive(
        tmp_path,
        {
            "kanji_meta_bank_10.json": [["三", "freq", {"value": 3, "displayValue": "3"}]],
            "kanji_meta_bank_2.json": [["二", "freq", {"value": 2, "displayValue": "2"}]],
        },
    )
    assert [entry[0] for entry in read_banks(archive, "kanji_meta_bank")] == ["二", "三"]


def test_keeps_entries_unchanged(tmp_path):
    entries = [
        ["猫", "freq", {"reading": "ねこ", "frequency": {"value": 1562, "displayValue": "1562"}}],
        ["猫", "freq", {"reading": "ねこ", "frequency": {"value": 18458, "displayValue": "18458㋕"}}],
    ]
    archive = _archive(tmp_path, {"term_meta_bank_1.json": entries})
    assert read_banks(archive, "term_meta_bank") == entries


def test_fails_on_other_banks(tmp_path):
    archive = _archive(tmp_path, {"term_meta_bank_1.json": [], "tag_bank_1.json": []})
    with pytest.raises(ValueError, match="tag_bank_1.json"):
        read_banks(archive, "term_meta_bank")


def test_fails_if_not_rank_based(tmp_path):
    archive = _archive(tmp_path, {"term_meta_bank_1.json": []}, mode="occurrence-based")
    with pytest.raises(ValueError, match="expected 'rank-based'"):
        read_banks(archive, "term_meta_bank")
