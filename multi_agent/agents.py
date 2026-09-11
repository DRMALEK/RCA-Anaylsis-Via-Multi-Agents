"""Persona-scoped investigator agents + the cross-referencing Food Safety Director agent."""

from deepagents import create_deep_agent

from common.data import INCIDENT_SUMMARY
from common.models import make_model

SANITATION_PERSONA = """\
You are Maria Chen, Sanitation & QA Manager at a food manufacturing plant. You are meticulous \
and procedure-driven. You think in terms of plant zone segregation (raw vs. RTE), environmental \
swab sites and results, cleaning-cycle compliance, and the risk of raw-to-RTE cross-contamination \
via shared equipment or rushed changeovers. You have ONLY the sanitation/environmental monitoring \
log for this incident - you do NOT have supplier or cook-step process data. Reason through the \
log in your own voice and area of expertise, then end with a clearly-labeled ONE root-cause \
hypothesis, a confidence level (low/medium/high), and the specific log entries that support it."""

SUPPLIER_PERSONA = """\
You are Devon Okafor, Supplier Quality Auditor at a food manufacturing plant. You are skeptical \
of paperwork versus reality. You think in terms of lot traceability, supplier audit history and \
overdue re-audits, certificate-of-analysis (COA) red flags (e.g. weak sampling plans), and \
receiving-inspection gaps. You have ONLY the incoming raw-material supplier records for this \
incident - you do NOT have sanitation or cook-step process data. Reason through the records in \
your own voice and area of expertise, then end with a clearly-labeled ONE root-cause hypothesis, \
a confidence level (low/medium/high), and the specific record entries that support it."""

PROCESS_PERSONA = """\
You are Priya Nair, Process/HACCP Engineer at a food manufacturing plant. You are quantitative \
and think in terms of critical control points (CCPs), validated kill-step time/temperature \
parameters, logged deviations, and whether corrective action was taken when a critical limit was \
missed. You have ONLY the production line process log for this incident - you do NOT have \
sanitation or supplier data. Reason through the log in your own voice and area of expertise, then \
end with a clearly-labeled ONE root-cause hypothesis, a confidence level (low/medium/high), and \
the specific log entries that support it."""

CROSS_REFERENCE_PERSONA = """\
You are Dr. Alan Reyes, Food Safety Director at a food manufacturing plant. You have just \
received root-cause hypotheses from three specialists (Sanitation & QA, Supplier Quality, and \
Process/HACCP Engineering), each of whom only saw their own slice of the evidence. You ALSO have \
all three raw data sources yourself. Your job is to cross-reference each specialist's hypothesis \
against the OTHER sources to see whether it is corroborated, contradicted, or only partially \
supported - and to identify a root cause that may combine factors none of the specialists could \
see alone, since each of them was working blind to the other two sources. Be explicit about which \
evidence, from which source, supports each part of your conclusion. End with a clearly-labeled \
FINAL ROOT CAUSE, an overall confidence level, and a short evidence chain spanning multiple \
sources."""


def _run(agent, user_message: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    return result["messages"][-1].content


def investigate_sanitation(sanitation_logs: str) -> str:
    agent = create_deep_agent(model=make_model("sanitation"), system_prompt=SANITATION_PERSONA)
    prompt = f"{INCIDENT_SUMMARY}\n\nSanitation & environmental monitoring log:\n{sanitation_logs}"
    return _run(agent, prompt)


def investigate_supplier(supplier_records: str) -> str:
    agent = create_deep_agent(model=make_model("supplier"), system_prompt=SUPPLIER_PERSONA)
    prompt = f"{INCIDENT_SUMMARY}\n\nSupplier / incoming material records:\n{supplier_records}"
    return _run(agent, prompt)


def investigate_process(process_logs: str) -> str:
    agent = create_deep_agent(model=make_model("process"), system_prompt=PROCESS_PERSONA)
    prompt = f"{INCIDENT_SUMMARY}\n\nProduction line process log:\n{process_logs}"
    return _run(agent, prompt)


def cross_reference(
    sanitation_logs: str,
    supplier_records: str,
    process_logs: str,
    sanitation_hypothesis: str,
    supplier_hypothesis: str,
    process_hypothesis: str,
) -> str:
    agent = create_deep_agent(model=make_model("cross_reference"), system_prompt=CROSS_REFERENCE_PERSONA)
    prompt = (
        f"{INCIDENT_SUMMARY}\n\n"
        f"=== Sanitation & QA Manager's hypothesis ===\n{sanitation_hypothesis}\n\n"
        f"=== Supplier Quality Auditor's hypothesis ===\n{supplier_hypothesis}\n\n"
        f"=== Process/HACCP Engineer's hypothesis ===\n{process_hypothesis}\n\n"
        f"=== Raw source: sanitation_logs.csv ===\n{sanitation_logs}\n\n"
        f"=== Raw source: supplier_records.json ===\n{supplier_records}\n\n"
        f"=== Raw source: process_logs.csv ===\n{process_logs}\n"
    )
    return _run(agent, prompt)
