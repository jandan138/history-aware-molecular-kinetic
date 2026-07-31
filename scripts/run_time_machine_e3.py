from __future__ import annotations

import argparse
import json
from pathlib import Path

from historykinetic.e3 import (
    load_e3_protocol,
    run_molecular_time_machine_e3,
    write_e3_result,
)
from historykinetic.e3.render import render_molecular_time_machine_e3


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the frozen One Collision, Two Worlds E3 recipe."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/studies/molecular-time-machine-e3-v0.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--no-trajectories", action="store_true")
    args = parser.parse_args()

    protocol = load_e3_protocol(args.config)
    result = run_molecular_time_machine_e3(protocol)
    paths = write_e3_result(
        result,
        args.output,
        protocol_path=args.config,
        include_trajectories=not args.no_trajectories,
    )
    if not args.skip_render:
        figure_svg, figure_pdf, video = render_molecular_time_machine_e3(
            result,
            args.output,
        )
        paths.update(
            {"figure_svg": figure_svg, "figure_pdf": figure_pdf, "video": video}
        )
    summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
    print(f"study: {protocol.study_id}")
    print(f"decision: {summary['decision']}")
    print(f"target: {result.target_event.event_id} {result.target_event.pair}")
    for name, path in sorted(paths.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
