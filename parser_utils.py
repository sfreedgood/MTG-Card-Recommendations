"""Orchestration helpers for site-specific MTG card parsers."""

from typing import Dict, Optional
from requests.exceptions import RequestException, HTTPError

from edhrec_parser import parse_edhrec_card_page


def parse_page(set_name: str, card_names: list[str]) -> Dict[str, Dict[str, Dict[str, Optional[str]]]]:
  results: Dict[str, Dict[str, Dict[str, Optional[str]]]] = {}

  for card_name in card_names:
    results[card_name] = {}

    try:
      results[card_name]["edhrec"] = parse_edhrec_card_page(card_name)
    except (HTTPError, RequestException, ValueError) as exc:
      results[card_name]["edhrec"] = {
        "source": "edhrec",
        "url": None,
        "error": type(exc).__name__,
        "error_message": str(exc),
      }

  return results

