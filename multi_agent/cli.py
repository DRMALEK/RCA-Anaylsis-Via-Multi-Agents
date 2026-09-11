"""CLI entry point for the multi-agent (persona-based) RCA demo."""

import argparse
from pathlib import Path

from common.data import load_all_sources
from multi_agent.graph import build_graph

NODE_LABELS = {
    "sanitation_investigator": "Maria Chen (Sanitation & QA Manager)",
    "supplier_investigator": "Devon Okafor (Supplier Quality Auditor)",
    "process_investigator": "Priya Nair (Process/HACCP Engineer)",
    "cross_reference": "Dr. Alan Reyes (Food Safety Director) - Cross-Referenced Conclusion",
}

HYPOTHESIS_KEYS = {
    "sanitation_investigator": "sanitation_hypothesis",
    "supplier_investigator": "supplier_hypothesis",
    "process_investigator": "process_hypothesis",
    "cross_reference": "final_report",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-agent salmonella RCA demo")
    parser.add_argument(
        "--out",
        default="rca_report_multi_agent.md",
        help="Path to write the final RCA report (default: rca_report_multi_agent.md)",
    )
    args = parser.parse_args()

    sources = load_all_sources()
    initial_state = {
        "sanitation_logs": sources["sanitation_logs.csv"],
        "supplier_records": sources["supplier_records.json"],
        "process_logs": sources["process_logs.csv"],
    }

    app = build_graph()
    final_report = ""

    print("Running multi-agent RCA investigation (3 investigators in parallel + cross-reference)...\n")
    for update in app.stream(initial_state, stream_mode="updates"):
        for node_name, node_output in update.items():
            label = NODE_LABELS.get(node_name, node_name)
            key = HYPOTHESIS_KEYS.get(node_name)
            text = node_output.get(key, "") if key else ""
            print(f"{'=' * 80}\n{label}\n{'=' * 80}\n{text}\n")
            if node_name == "cross_reference":
                final_report = text

    out_path = Path(args.out)
    out_path.write_text(final_report, encoding="utf-8")
    print(f"Final RCA report written to {out_path.resolve()}")


if __name__ == "__main__":
    main()
