"""EDHREC-specific parsing for a single card page."""

import re
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, RequestException

from url_utils import build_edhrec_card_url


def _text_or_none(node) -> Optional[str]:
    return node.get_text(strip=True) if node else None


def _extract_price(card) -> Optional[float]:
    """Extract Cardmarket price from a BeautifulSoup card container element."""
    cardmarket_link = card.find("a", title="Buy at Cardmarket")
    if not cardmarket_link:
        return None

    price_span = cardmarket_link.find("span")
    raw = _text_or_none(price_span)
    if not raw:
        return None

    normalized = raw.replace("€", "").replace(",", ".").strip()
    try:
        return float(normalized)
    except ValueError:
        return None


def _extract_section_cards(soup, section_id: str) -> List[Dict[str, Any]]:
    section = soup.find("div", id=section_id)
    if not section:
        return []

    cards = section.find_all(
        lambda tag: tag.name == "div"
        and any(c.startswith("Card_container") for c in (tag.get("class") or []))
    )

    return [
        {
            "name": _text_or_none(
                card.find(
                    lambda tag: tag.name == "span"
                    and any(c.startswith("Card_name") for c in (tag.get("class") or []))
                )
            ),
            "price": _extract_price(card),
        }
        for card in cards
    ]


def _safe_http_get(url: str, timeout: int = 15) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MTG-Scraper/1.0; +https://localhost.localdomain)"
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    response.encoding = response.encoding or "utf-8"
    return response.text


def parse_edhrec_card_page(card_name: str) -> Dict[str, Any]:
    """Parse an EDHREC card page. Returns error dict on failure."""
    url = build_edhrec_card_url(card_name)

    try:
        html = _safe_http_get(url)
        soup = BeautifulSoup(html, "html.parser")

        canonical = soup.find("link", rel="canonical")

        return {
            "source": "edhrec",
            "url": url,
            "page_title": _text_or_none(soup.find("title")),
            "top_cards": _extract_section_cards(soup, "topcards"),
            "top_commanders": _extract_section_cards(soup, "topcommanders"),
            "high_lift": _extract_section_cards(soup, "highliftcards"),
            "canonical_url": canonical["href"] if canonical else None,
        }
    except (HTTPError, RequestException, ValueError) as exc:
        return {
            "source": "edhrec",
            "url": url,
            "error": type(exc).__name__,
            "error_message": str(exc),
        }