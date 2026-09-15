"""A single generalist deep agent given all raw data sources at once (no orchestration)."""

from deepagents import create_deep_agent

from common.data import INCIDENT_SUMMARY, load_all_sources
from common.metrics import RunMetrics, timed_invoke
from common.models import make_model

SYSTEM_PROMPT = """\
You are a food safety root-cause analyst at a food manufacturing plant. You have been given \
ALL available evidence for a Salmonella-positive finished product incident: sanitation and \
environmental monitoring logs, supplier/incoming material records, and the production line \
process log. Investigate across all three sources yourself, cross-referencing any relevant \
details between them, and produce a root-cause analysis. End with a clearly-labeled FINAL ROOT \
CAUSE, an overall confidence level, and a short evidence chain citing the specific sources and \
entries that support your conclusion."""


def run_single_agent() -> tuple[str, RunMetrics]:
    sources = load_all_sources()
    agent = create_deep_agent(model=make_model("single_agent"), system_prompt=SYSTEM_PROMPT)
    prompt = (
        f"{INCIDENT_SUMMARY}\n\n"
        f"=== sanitation_logs.csv ===\n{sources['sanitation_logs.csv']}\n\n"
        f"=== supplier_records.json ===\n{sources['supplier_records.json']}\n\n"
        f"=== process_logs.csv ===\n{sources['process_logs.csv']}\n"
    )
    return timed_invoke(agent, prompt, "Single Agent (generalist)")
