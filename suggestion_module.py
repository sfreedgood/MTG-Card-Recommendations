"""Helpers for combining EDHREC suggestion lists into ranked counts."""

from collections import Counter
from typing import Dict, List, Tuple

from edhrec_parser import parse_edhrec_card_page

SuggestionCount = List[Dict[str, int]]


def consolidate_edhrec_lists(
    card_names: List[str]
) -> List[Tuple[str, int, float]]:
    """
    Fetch EDHREC data for each card and rank suggestions by frequency across
    high_lift, top_commanders, and top_cards sections.
    """
    counter: Counter[str] = Counter()
    card_names_set = set(card_names)

    for card_name in card_names:
        parsed = parse_edhrec_card_page(card_name)
        
        # Skip if error occurred
        if "error" in parsed:
            continue

        for section in ("high_lift", "top_commanders", "top_cards"):
            cards = parsed.get(section, [])
            for card in cards:
                if isinstance(card, dict):
                    name = card.get("name")
                    if isinstance(name, str) and name.strip():
                        stripped_name = name.strip()
                        if stripped_name not in card_names_set:
                            counter[stripped_name] += 1

    return sorted(
        [(name, count) for name, count in counter.items()],
        key=lambda item: (-item[1], item[0])
    )


def consolidate_to_mapping(card_names: List[str]) -> SuggestionCount:
    """Return a ranked list of dicts with count, ordered by count desc."""
    return [
        {name: count}
        for name, count, in consolidate_edhrec_lists(card_names)
        if count > 1
    ]