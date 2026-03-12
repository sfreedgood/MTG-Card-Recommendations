"""CLI entrypoint to parse Cardmarket and EDHREC card pages."""

import argparse
import json
import warnings
from urllib3.exceptions import NotOpenSSLWarning

from parser_utils import parse_page
from suggestion_module import consolidate_to_mapping

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch MTG card data from EDHREC")
    parser.add_argument("--set", required=False, help="Card set name, e.g. 'Zendikar Rising'")
    parser.add_argument("--card", required=False, help="Card name, e.g. 'Teferi, Master of Time'")
    parser.add_argument("--csv", required=False, help="Path to CSV file with card names (single column)")
    
    args = parser.parse_args()
    if not args.card and not args.csv:
        parser.error("Either --card or --csv must be provided")
    return args


def main() -> None:
    args = parse_args()
    data = consolidate_to_mapping(args.csv.split(',')) if args.csv else parse_page(args.set, [args.card])
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
