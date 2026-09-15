# RCA Analysis via Multi-Agents

A small demo of multi-agent orchestration with [LangGraph's `deepagents`](https://github.com/langchain-ai/deepagents),
applied to root-cause analysis (RCA) of a **Salmonella contamination incident at a food
manufacturing plant**. 

Two versions are included so you can compare persona-based multi-agent orchestration against a single generalist agent on identical data.

Models are free-tier models served via [OpenRouter](https://openrouter.ai/).

## The scenario

A ready-to-eat (RTE) chicken product from Line 2 tests positive for Salmonella. Evidence is spread
across three data sources in `data/`:

- `sanitation_logs.csv` — environmental swabs & cleaning-cycle records
- `supplier_records.json` — incoming raw-material lots, supplier COAs, audit history
- `process_logs.csv` — cook/chill step (CCP) time-temperature log

No single source is conclusive alone — the real root cause only emerges by cross-referencing all
three.

## Version 1 — Multi-agent (`multi_agent/`)

```
                 ┌─────────────────────────┐
       ┌────────▶│ Maria Chen              │──┐
       │         │ Sanitation & QA Manager │  │
       │         └─────────────────────────┘  │
       │         ┌─────────────────────────┐  │      ┌──────────────────────────┐
 START ┼────────▶│ Devon Okafor            │──┼─────▶│ Dr. Alan Reyes           │──▶ END
       │         │ Supplier Quality Auditor│  │      │ Food Safety Director     │
       │         └─────────────────────────┘  │      │ (cross-references all 3 │
       │         ┌─────────────────────────┐  │      │  hypotheses + sources)  │
       └────────▶│ Priya Nair              │──┘      └──────────────────────────┘
                 │ Process/HACCP Engineer  │
                 └─────────────────────────┘
```

Three investigator deep agents each get **only their own data source** and a distinct persona,
and propose one root-cause hypothesis in their own voice. A fourth deep agent (the Food Safety
Director) receives all three hypotheses plus all raw sources, and cross-references them to reach
a final root cause that may combine factors no single investigator could see alone.

Run it:

```bash
python multi_agent_main.py
```

## Version 2 — Single-agent baseline (`single_agent/`)

One generalist deep agent is given all three raw data sources at once and asked to produce the
RCA report directly — no persona split, no orchestration.

Run it:

```bash
python single_agent_main.py
```

## What to compare

Run both and look at `rca_report_multi_agent.md` vs. `rca_report_single_agent.md`. Both should
converge on roughly the same underlying root cause (a partial kill-step deviation combined with a
raw→RTE cross-contamination path via a rushed, uncleaned equipment changeover) — but the
multi-agent version's trace shows each specialist reasoning independently from a narrower view
before a dedicated cross-reference step combines them, versus a single agent reasoning over
everything at once.

## Token usage & latency

Both CLIs track token usage (input/output/total) and wall-clock latency for every deep-agent LLM
call. After a run finishes, a summary table is printed to the console, e.g.:

```
================================================================================
Metrics Summary
================================================================================
Agent                                               Calls        In       Out     Total  Latency(s)
--------------------------------------------------------------------------------------------------
Maria Chen (Sanitation & QA Manager)                    2       842       310      1152        4.31
Devon Okafor (Supplier Quality Auditor)                 2       901       275      1176        3.98
Priya Nair (Process/HACCP Engineer)                     3      1204       402      1606        6.12
Dr. Alan Reyes (Food Safety Director) - ...             2      2380       540      2920        7.45
--------------------------------------------------------------------------------------------------
TOTAL                                                    9      5327      1527      6854       21.86
```

The same data is written to `metrics_multi_agent.json` / `metrics_single_agent.json` (one entry per
agent), so you can compare the cost/latency overhead of the orchestrated fan-out-then-join pipeline
against the single generalist agent. Both files are gitignored since they're per-run output.

Note: since the default models are free-tier, this tracks token counts and latency rather than
dollar cost — swap in paid model IDs (see below) if you want to translate token counts into cost.

## Setup

1. `pip install -r requirements.txt`
2. Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys)
3. Copy `.env.example` to `.env` and set `OPENROUTER_API_KEY`
4. Run either `python multi_agent_main.py` or `python single_agent_main.py`

Per-role model IDs can be overridden via env vars — see `.env.example`.

Both CLIs also accept `--out <path>` (report destination) and `--metrics-out <path>` (metrics JSON
destination) to override the default filenames.
