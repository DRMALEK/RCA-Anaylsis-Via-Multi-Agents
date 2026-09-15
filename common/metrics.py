"""Token-usage and latency tracking for deep-agent runs."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter

from langchain_core.messages import AIMessage


@dataclass
class RunMetrics:
    label: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    llm_calls: int = 0
    latency_s: float = 0.0


def _extract_usage(messages) -> tuple[int, int, int, int]:
    input_tokens = output_tokens = total_tokens = llm_calls = 0
    for msg in messages:
        usage = getattr(msg, "usage_metadata", None) if isinstance(msg, AIMessage) else None
        if not usage:
            continue
        input_tokens += usage.get("input_tokens", 0)
        output_tokens += usage.get("output_tokens", 0)
        total_tokens += usage.get("total_tokens", 0)
        llm_calls += 1
    return input_tokens, output_tokens, total_tokens, llm_calls


def timed_invoke(agent, user_message: str, label: str) -> tuple[str, RunMetrics]:
    """Invoke a deep agent, timing it and summing token usage across every LLM call it made."""
    start = perf_counter()
    result = agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    latency_s = perf_counter() - start

    input_tokens, output_tokens, total_tokens, llm_calls = _extract_usage(result["messages"])
    metrics = RunMetrics(
        label=label,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        llm_calls=llm_calls,
        latency_s=latency_s,
    )
    return result["messages"][-1].content, metrics


def print_summary(metrics_list: list[RunMetrics]) -> None:
    header = f"{'Agent':<50}{'Calls':>7}{'In':>10}{'Out':>10}{'Total':>10}{'Latency(s)':>12}"
    print(f"{'=' * 80}\nMetrics Summary\n{'=' * 80}")
    print(header)
    print("-" * len(header))

    totals = {"llm_calls": 0, "input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "latency_s": 0.0}
    for m in metrics_list:
        print(f"{m.label:<50}{m.llm_calls:>7}{m.input_tokens:>10}{m.output_tokens:>10}{m.total_tokens:>10}{m.latency_s:>12.2f}")
        totals["llm_calls"] += m.llm_calls
        totals["input_tokens"] += m.input_tokens
        totals["output_tokens"] += m.output_tokens
        totals["total_tokens"] += m.total_tokens
        totals["latency_s"] += m.latency_s

    print("-" * len(header))
    print(
        f"{'TOTAL':<50}{totals['llm_calls']:>7}{totals['input_tokens']:>10}"
        f"{totals['output_tokens']:>10}{totals['total_tokens']:>10}{totals['latency_s']:>12.2f}\n"
    )


def write_metrics_json(metrics_list: list[RunMetrics], path) -> None:
    Path(path).write_text(json.dumps([asdict(m) for m in metrics_list], indent=2), encoding="utf-8")
