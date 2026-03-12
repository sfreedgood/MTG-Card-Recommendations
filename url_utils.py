"""Helpers for building MTG URL targets."""

import re
import unicodedata
from urllib.parse import quote


def to_hyphenated_slug(value: str) -> str:
    """
    Convert a set/card name to the slug format used in the target URLs.
    Examples:
      "Zendikar Rising" -> "zendikar-rising"
      "Golos, Tireless Pilgrim" -> "golos-tireless-pilgrim"
    """

    if not isinstance(value, str):
        raise TypeError("value must be a string")

    text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"\s*&\s*", " and ", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")

def build_edhrec_card_url(card_name: str) -> str:
    card_slug = to_hyphenated_slug(card_name)
    return f"https://edhrec.com/cards/{card_slug}"
