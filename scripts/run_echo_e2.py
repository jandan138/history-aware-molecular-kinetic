from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

from historykinetic.e2 import load_e2_protocol, render_e2, run_e2, write_e2_result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the preregistered Molecular Echoes E2 mechanism experiment."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/studies/molecular-echoes-e2-v0.json"),
    )
    parser.add_argument(
        "--calibration",
        type=Path,
        default=Path("results/molecular-echoes-e2-v0/calibration-dose-only.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="run one small pipeline case; never use as scientific evidence",
    )
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--no-trajectories", action="store_true")
    args = parser.parse_args()

    protocol = load_e2_protocol(args.config)
    if protocol.selected_budget.branch_name not in args.calibration.read_text(
        encoding="utf-8"
    ):
        raise ValueError("frozen selected budget does not match calibration artifact")
    if args.smoke:
        e1 = protocol.e1_protocol
        smoke_seed = protocol.seeds[0]
        smoke_size = replace(e1.sizes[0], count=32, diameter=5.12 / 32)
        e1 = replace(
            e1,
            sizes=(smoke_size,),
            seeds=(smoke_seed,),
            preparation_time=0.2,
            future_horizon=0.2,
            sample_interval=0.05,
            bootstrap_resamples=200,
            render=replace(e1.render, hero_particle_count=32),
        )
        protocol = replace(
            protocol,
            e1_protocol=e1,
            seeds=(smoke_seed,),
            calibration_particle_count=32,
            bootstrap_resamples=200,
            render=replace(protocol.render, hero_particle_count=32),
        )
    result = run_e2(protocol)
    paths = write_e2_result(
        result,
        args.output,
        protocol_path=args.config,
        calibration_path=args.calibration,
        include_trajectories=not args.no_trajectories,
    )
    if not args.skip_render:
        svg, pdf, video = render_e2(result, args.output)
        paths.update({"figure_svg": svg, "figure_pdf": pdf, "video": video})
    summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
    print(f"study: {protocol.study_id}")
    print(f"cases: {len(result.cases)}")
    print(f"decision: {summary['decision']}")
    for name, path in sorted(paths.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
