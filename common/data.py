"""Loads the bundled salmonella-incident data sources."""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_sanitation_logs() -> str:
    return (DATA_DIR / "sanitation_logs.csv").read_text(encoding="utf-8")


def load_supplier_records() -> str:
    return (DATA_DIR / "supplier_records.json").read_text(encoding="utf-8")


def load_process_logs() -> str:
    return (DATA_DIR / "process_logs.csv").read_text(encoding="utf-8")


def load_all_sources() -> dict[str, str]:
    return {
        "sanitation_logs.csv": load_sanitation_logs(),
        "supplier_records.json": load_supplier_records(),
        "process_logs.csv": load_process_logs(),
    }


INCIDENT_SUMMARY = (
    "Incident: A ready-to-eat (RTE) chicken product from Line 2, produced on 2026-08-10, "
    "tested positive for Salmonella in finished-goods testing. Determine the root cause."
)
