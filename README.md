# japanese-jiten-frequency-yomitan

Jiten's word and kanji frequency lists for Yomitan and DaKanji

## Sources

Where the data comes from and how the dictionary is derived from it.

The sources are locked to a version in `sources.lock.json`.
The *Update* workflow checks them weekly, commits newer versions and releases the dictionary if it changed.

## Installation

Make sure [uv](https://github.com/astral-sh/uv) is installed on your system and run

``` bash
uv sync
```

## Usage

``` bash
uv run build.py
```

This creates the dictionary in `out/` (`japanese-jiten-frequency-yomitan.zip`, `japanese-jiten-frequency-yomitan.index.json` and `japanese-jiten-frequency-yomitan.manifest.json`).
Downloaded sources are cached in `tmp/sources/`, the uncompressed dictionary is kept in `tmp/japanese-jiten-frequency-yomitan/` for inspection.

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
