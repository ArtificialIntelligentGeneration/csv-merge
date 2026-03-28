"""csv-merge — merge multiple CSV files by a shared key column."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import OrderedDict
from pathlib import Path


def merge(files: list[Path], key: str, how: str, sep: str, encoding: str) -> tuple[list[str], list[dict]]:
    """Return (header, rows) where rows is a list of merged dicts keyed by `key`."""
    by_key: dict[str, dict] = OrderedDict()
    headers_seen: list[str] = [key]
    files_keys: list[set[str]] = []

    for path in files:
        with path.open(newline="", encoding=encoding) as fh:
            reader = csv.DictReader(fh, delimiter=sep)
            if reader.fieldnames is None or key not in reader.fieldnames:
                raise SystemExit(f"{path}: missing key column '{key}'")
            for col in reader.fieldnames:
                if col != key and col not in headers_seen:
                    headers_seen.append(col)
            file_keys: set[str] = set()
            for row in reader:
                k = row[key]
                file_keys.add(k)
                merged = by_key.setdefault(k, {key: k})
                for col, val in row.items():
                    if col == key:
                        continue
                    merged[col] = val
            files_keys.append(file_keys)

    if how == "inner":
        common = set.intersection(*files_keys) if files_keys else set()
        rows = [r for k, r in by_key.items() if k in common]
    else:
        rows = list(by_key.values())

    return headers_seen, rows


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Merge CSV files by a shared key column.")
    p.add_argument("--key", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--how", choices=("outer", "inner"), default="outer")
    p.add_argument("--sep", default=",")
    p.add_argument("--encoding", default="utf-8")
    p.add_argument("files", nargs="+", type=Path)
    args = p.parse_args(argv)

    header, rows = merge(args.files, args.key, args.how, args.sep, args.encoding)
    with Path(args.output).open("w", newline="", encoding=args.encoding) as fh:
        writer = csv.DictWriter(fh, fieldnames=header, extrasaction="ignore", delimiter=args.sep)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\u2713 merged {len(args.files)} files ({len(rows)} rows) \u2192 {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
