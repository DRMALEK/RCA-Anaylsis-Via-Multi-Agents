"""CLI entry point for the single-agent RCA baseline (no multi-agent orchestration)."""

import argparse
from pathlib import Path

from common.metrics import print_summary, write_metrics_json
from single_agent.agent import run_single_agent


def main() -> None:
    parser = argparse.ArgumentParser(description="Single-agent salmonella RCA baseline")
    parser.add_argument(
        "--out",
        default="rca_report_single_agent.md",
        help="Path to write the final RCA report (default: rca_report_single_agent.md)",
    )
    parser.add_argument(
        "--metrics-out",
        default="metrics_single_agent.json",
        help="Path to write token/latency metrics (default: metrics_single_agent.json)",
    )
    args = parser.parse_args()

    print("Running single-agent RCA investigation (one generalist agent, all sources)...\n")
    report, metrics = run_single_agent()
    print(f"{'=' * 80}\nFinal Report\n{'=' * 80}\n{report}\n")

    out_path = Path(args.out)
    out_path.write_text(report, encoding="utf-8")
    print(f"Final RCA report written to {out_path.resolve()}")

    print_summary([metrics])
    metrics_out_path = Path(args.metrics_out)
    write_metrics_json([metrics], metrics_out_path)
    print(f"Metrics written to {metrics_out_path.resolve()}")


if __name__ == "__main__":
    main()
