from __future__ import annotations

import argparse
from pathlib import Path

from historykinetic.studies.matched_pairs import matched_pairs_from_dataset


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find matched-state/different-history pairs for the Phase-I main figure."
    )
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=24)
    parser.add_argument("--maximum-state-distance", type=float, default=0.5)
    args = parser.parse_args()
    output = matched_pairs_from_dataset(
        args.dataset,
        args.output,
        limit=args.limit,
        maximum_state_distance=args.maximum_state_distance,
    )
    print(f"matched-pair candidates: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
