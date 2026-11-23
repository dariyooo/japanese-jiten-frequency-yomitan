# japanese-jiten-frequency-yomitan

Jiten's word and kanji frequency lists for Yomitan and DaKanji.

[Jiten](https://jiten.moe) ranks words and kanji by how often they appear in its corpus of Japanese media
(about 4 billion characters from anime subtitles, novels, visual novels, games, manga and more).
This repo republishes its global word list and its kanji list as pinned, attributed releases, which DaKanji's
database build downloads.

| Asset | Title | Content |
|---|---|---|
| `japanese-jiten-frequency-yomitan-terms.zip` | Jiten Frequency | `term_meta_bank`, rank-based |
| `japanese-jiten-frequency-yomitan-kanji.zip` | Jiten Frequency (Kanji) | `kanji_meta_bank`, rank-based |

The entries are Jiten's, unchanged. Like JPDB's frequency list, a word written in kanji has two ranks:
as written (`1562`) and written in kana (`18458㋕`).

**Using Yomitan?** Install Jiten's own lists from [jiten.moe/frequency-dictionaries](https://jiten.moe/frequency-dictionaries),
they also cover single media types (anime, novels, ...). This repo only adds pinned releases and attribution.

## Sources

* Jiten's frequency lists from its API (`api.jiten.moe/api/frequency-list/download` and `/download-kanji`).
  Jiten publishes no versions, so they are locked by sha256 in `sources.lock.json` and versioned by download date.
  The *Update* workflow downloads them weekly and releases if they changed.
* Only `index.json` is replaced: titles that do not clash with Jiten's own lists, attribution and license, and update
  URLs pointing to this repo. Each release keeps a full copy, so the database build keeps working if Jiten changes its API.

## Installation

Make sure [uv](https://github.com/astral-sh/uv) is installed on your system and run

``` bash
uv sync
```

## Usage

``` bash
uv run build.py
```

This creates both dictionaries in `out/`, each as `.zip`, `.index.json` and `.manifest.json`.
Downloaded sources are cached in `tmp/sources/`, the uncompressed dictionaries are kept in `tmp/japanese-jiten-frequency-yomitan-{terms,kanji}/` for inspection.

## Development

``` bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run pyright               # type check
uv run pytest                # tests
```

The repo follows the [DaLang dictionary repo standard](https://github.com/dariyooo/dalang-dict-utils/blob/main/docs/repo-standard.md),
update the shared setup with `uvx copier update --trust`.

## Release

Push a tag with today's date:

``` bash
git tag 2026-11-01 && git push origin 2026-11-01
```

The *Release* workflow runs the checks, builds the dictionary with the tag as revision and publishes it as the GitHub release of the tag.
To redo a release, push the tag again with `git tag -f 2026-11-01 && git push -f origin 2026-11-01`.
Installed dictionaries pick up new releases through "Check for updates".

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), as required by Jiten's frequency lists (CC BY-SA 4.0, [jiten.moe](https://jiten.moe)).
Jiten builds on JMdict and KANJIDIC by the [EDRDG](https://www.edrdg.org/edrdg/licence.html) (CC BY-SA 4.0).
