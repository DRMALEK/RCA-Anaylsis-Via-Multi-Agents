"""LangGraph StateGraph: 3 investigators fan out in parallel, then join into cross-reference."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from common.metrics import RunMetrics
from multi_agent.agents import (
    cross_reference,
    investigate_process,
    investigate_sanitation,
    investigate_supplier,
)


class RCAState(TypedDict):
    sanitation_logs: str
    supplier_records: str
    process_logs: str
    sanitation_hypothesis: str
    supplier_hypothesis: str
    process_hypothesis: str
    final_report: str
    sanitation_metrics: RunMetrics
    supplier_metrics: RunMetrics
    process_metrics: RunMetrics
    cross_reference_metrics: RunMetrics


def _sanitation_node(state: RCAState) -> dict:
    hypothesis, metrics = investigate_sanitation(state["sanitation_logs"])
    return {"sanitation_hypothesis": hypothesis, "sanitation_metrics": metrics}


def _supplier_node(state: RCAState) -> dict:
    hypothesis, metrics = investigate_supplier(state["supplier_records"])
    return {"supplier_hypothesis": hypothesis, "supplier_metrics": metrics}


def _process_node(state: RCAState) -> dict:
    hypothesis, metrics = investigate_process(state["process_logs"])
    return {"process_hypothesis": hypothesis, "process_metrics": metrics}


def _cross_reference_node(state: RCAState) -> dict:
    report, metrics = cross_reference(
        sanitation_logs=state["sanitation_logs"],
        supplier_records=state["supplier_records"],
        process_logs=state["process_logs"],
        sanitation_hypothesis=state["sanitation_hypothesis"],
        supplier_hypothesis=state["supplier_hypothesis"],
        process_hypothesis=state["process_hypothesis"],
    )
    return {"final_report": report, "cross_reference_metrics": metrics}


def build_graph():
    graph = StateGraph(RCAState)
    graph.add_node("sanitation_investigator", _sanitation_node)
    graph.add_node("supplier_investigator", _supplier_node)
    graph.add_node("process_investigator", _process_node)
    graph.add_node("cross_reference", _cross_reference_node)

    graph.add_edge(START, "sanitation_investigator")
    graph.add_edge(START, "supplier_investigator")
    graph.add_edge(START, "process_investigator")
    graph.add_edge("sanitation_investigator", "cross_reference")
    graph.add_edge("supplier_investigator", "cross_reference")
    graph.add_edge("process_investigator", "cross_reference")
    graph.add_edge("cross_reference", END)

    return graph.compile()
