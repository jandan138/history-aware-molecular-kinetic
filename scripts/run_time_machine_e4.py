from __future__ import annotations

import argparse
import json
from pathlib import Path

from historykinetic.e4 import (
    load_e4_protocol,
    run_molecular_time_machine_e4,
    write_e4_result,
)
from historykinetic.e4.render import render_molecular_time_machine_e4


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the frozen Choose the Cause, Direct the Future E4 recipe."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/studies/molecular-time-machine-e4-v0.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--no-trajectories", action="store_true")
    args = parser.parse_args()

    protocol = load_e4_protocol(args.config)
    result = run_molecular_time_machine_e4(protocol)
    paths = write_e4_result(
        result,
        args.output,
        protocol_path=args.config,
        include_trajectories=not args.no_trajectories,
    )
    if not args.skip_render:
        figure_svg, figure_pdf, video, viewer = render_molecular_time_machine_e4(
            result,
            args.output,
        )
        paths.update(
            {
                "figure_svg": figure_svg,
                "figure_pdf": figure_pdf,
                "video": video,
                "viewer": viewer,
            }
        )
    summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
    print(f"study: {protocol.study_id}")
    print(f"decision: {summary['decision']}")
    print(
        "selected: "
        f"{result.selected_preview.candidate.event.event_id} "
        f"{result.selected_preview.candidate.event.pair} "
        f"{result.selected_preview.angle_degrees:+g} degrees"
    )
    for name, path in sorted(paths.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
