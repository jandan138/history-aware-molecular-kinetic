from __future__ import annotations

import argparse
import json
from pathlib import Path

from historykinetic.e5 import load_e5_protocol, run_molecular_time_machine_e5
from historykinetic.e5.artifacts import write_e5_result
from historykinetic.e5.render import render_molecular_time_machine_e5


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the frozen Same Present, Chosen Future E5 recipe."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/studies/molecular-time-machine-e5-v0.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--no-trajectories", action="store_true")
    args = parser.parse_args()

    protocol = load_e5_protocol(args.config)
    result = run_molecular_time_machine_e5(protocol)
    paths = write_e5_result(
        result,
        args.output,
        protocol_path=args.config,
        include_trajectories=not args.no_trajectories,
    )
    if not args.skip_render:
        figure_svg, figure_pdf, video, viewer = render_molecular_time_machine_e5(
            result, args.output
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
    print(f"selected swaps: {result.selected_preview.surgery.swaps}")
    print(
        "future: "
        f"target reduction {result.metrics.target_region_reduction_fraction:.0%}, "
        f"collateral retention {result.metrics.collateral_retention_fraction:.0%}"
    )
    for name, path in sorted(paths.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
