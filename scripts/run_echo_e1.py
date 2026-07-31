from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

from historykinetic.echo import load_echo_protocol, run_echo_e1
from historykinetic.echo.artifacts import write_echo_e1_result
from historykinetic.echo.render import render_echo_e1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the preregistered Molecular Echoes E1 story experiment."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/studies/molecular-echoes-e1-v0.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="run one small case for pipeline verification; never primary evidence",
    )
    parser.add_argument(
        "--skip-render",
        action="store_true",
        help="write scientific artifacts without the SVG/PDF/video outputs",
    )
    parser.add_argument(
        "--no-trajectories",
        action="store_true",
        help="omit the compressed trajectory bundle",
    )
    args = parser.parse_args()

    protocol = load_echo_protocol(args.config)
    if args.smoke:
        first_size = protocol.sizes[0]
        protocol = replace(
            protocol,
            sizes=(replace(first_size, count=32, diameter=5.12 / 32),),
            seeds=(protocol.seeds[0],),
            preparation_time=0.2,
            future_horizon=0.2,
            sample_interval=0.05,
            bootstrap_resamples=200,
            render=replace(protocol.render, hero_particle_count=32),
        )
    result = run_echo_e1(protocol)
    paths = write_echo_e1_result(
        result,
        args.output,
        protocol_path=args.config,
        include_trajectories=not args.no_trajectories,
    )
    if not args.skip_render:
        figure_svg, figure_pdf, video = render_echo_e1(result, args.output)
        paths.update(
            {
                "figure_svg": figure_svg,
                "figure_pdf": figure_pdf,
                "video": video,
            }
        )
    summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
    print(f"study: {protocol.study_id}")
    print(f"cases: {len(result.cases)}")
    print(f"decision: {summary['decision']}")
    for name, path in sorted(paths.items()):
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
