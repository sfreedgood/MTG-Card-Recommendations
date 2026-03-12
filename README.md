# MTG Card Recommendations (EDHREC scraper)

A small Python playground + command-line utility that scrapes EDHREC pages to surface high-synergy card suggestions for a partial decklist.

> Note: This is a personal project / playground. EDHREC is a third-party site; scraping can break if the site changes and may be subject to their Terms of Service and rate limits.

## What’s in here
- `run.py` — CLI entrypoint
- `edhrec_parser.py` — EDHREC page scraping/parsing
- `suggestion_module.py` — consolidates parsed results into a mapping
- `parser_utils.py`, `url_utils.py` — helpers

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
### Single card
```bash
python run.py --card "Teferi, Master of Time"
```

### CSV input
`--csv` currently expects a comma-separated list of CSV file paths (see `run.py`).

```bash
python run.py --csv cards.csv
```

The script prints JSON to stdout.

## Output
The CLI prints a JSON mapping (pretty-printed) of the parsed/suggested card data.

## Roadmap ideas
- Add a real decklist parser (Moxfield/Archidekt/Deckstats export)
- Cache HTTP responses and add polite request throttling
- Add tests for parsing logic
