import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path

from dalang_dict import Url, build_index, fetch, package_dictionary, used_sources

GITHUB_REPO = "dariyooo/japanese-jiten-frequency-yomitan"
ASSET = "japanese-jiten-frequency-yomitan"
JITEN_API = "https://api.jiten.moe/api/frequency-list"
BANK_FILE = re.compile(r"^(?P<bank>[a-z_]+)_(?P<number>\d+)\.json$")

# Jiten publishes no versions: the lists are locked by sha256 in sources.lock.json and versioned by download date.
# The Update workflow downloads them weekly and releases if they changed.
TERMS = Url(
    "jiten_freq_global.zip",
    f"{JITEN_API}/download",
    used_for="word frequency ranks of all media (term_meta_bank), unchanged",
)
KANJI = Url(
    "jiten_kanji_freq.zip",
    f"{JITEN_API}/download-kanji",
    used_for="kanji frequency ranks of all media (kanji_meta_bank), unchanged",
)

ATTRIBUTION = (
    "Frequency data: Jiten (https://jiten.moe), CC BY-SA 4.0. "
    "Built on JMdict and KANJIDIC by the Electronic Dictionary Research and Development Group (EDRDG), CC BY-SA 4.0."
)


@dataclass(frozen=True)
class Dictionary:
    variant: str
    source: Url
    bank: str
    title: str
    description: str


DICTIONARIES = [
    Dictionary(
        "terms",
        TERMS,
        "term_meta_bank",
        "Jiten Frequency",
        "Word frequency ranks from all media on jiten.moe (anime, novels, visual novels, games, ...). "
        "A word written in kanji has two ranks: as written, and written in kana (㋕).",
    ),
    Dictionary(
        "kanji",
        KANJI,
        "kanji_meta_bank",
        "Jiten Frequency (Kanji)",
        "Kanji frequency ranks from all media on jiten.moe (anime, novels, visual novels, games, ...).",
    ),
]

INDEX_FIELDS = {
    "sourceLanguage": "ja",
    "frequencyMode": "rank-based",
    "author": "Jiten (jiten.moe)",
    "url": f"https://github.com/{GITHUB_REPO}",
    "attribution": ATTRIBUTION,
}


def read_banks(archive: Path, bank: str) -> list:
    """Reads the entries of every `{bank}_{n}.json` of a Jiten zip in order, fails on other banks.

    Also fails if Jiten's list is no longer rank-based, its values would then be passed on with the wrong meaning.
    """
    with zipfile.ZipFile(archive) as zipf:
        mode = json.loads(zipf.read("index.json")).get("frequencyMode")
        if mode != "rank-based":
            raise ValueError(f"'{archive}' is {mode!r}, expected 'rank-based'")
        banks = [match for name in zipf.namelist() if (match := BANK_FILE.match(name))]
        other = sorted(match.string for match in banks if match["bank"] != bank)
        if other or not banks:
            raise ValueError(f"'{archive}' has {other or 'no'} banks, expected only '{bank}'")
        files = [match.string for match in sorted(banks, key=lambda match: int(match["number"]))]
        return [entry for name in files for entry in json.loads(zipf.read(name))]


def build_dictionary_index(dictionary: Dictionary) -> dict:
    return build_index(
        dictionary.title,
        GITHUB_REPO,
        f"{ASSET}-{dictionary.variant}",
        description=dictionary.description,
        **INDEX_FIELDS,
    )


def main() -> None:
    for dictionary in DICTIONARIES:
        entries = read_banks(fetch(dictionary.source), dictionary.bank)
        sources = {dictionary.source.name: used_sources()[dictionary.source.name]}
        package_dictionary(
            f"{ASSET}-{dictionary.variant}",
            build_dictionary_index(dictionary),
            {dictionary.bank: entries},
            sources=sources,
        )
