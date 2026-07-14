"""Command-line entry points."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .inventory import flatten_inventory, manifest_provenance, write_jsonl


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    normalize = subparsers.add_parser("normalize")
    normalize.add_argument("input", type=Path)
    normalize.add_argument("output", type=Path)
    normalize.add_argument("--provenance", type=Path)
    args = parser.parse_args()

    document = json.loads(args.input.read_text(encoding="utf-8"))
    records = flatten_inventory(document)
    write_jsonl(records, args.output)
    if args.provenance:
        args.provenance.parent.mkdir(parents=True, exist_ok=True)
        args.provenance.write_text(
            json.dumps(manifest_provenance(args.input), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(f"wrote {len(records)} canonical URL records to {args.output}")


if __name__ == "__main__":
    main()
