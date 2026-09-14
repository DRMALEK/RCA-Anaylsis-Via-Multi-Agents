# Findings: Single-Agent vs Multi-Agent RCA

Comparison based on `rca_report_single_agent.md` and `rca_report_multi_agent.md` (Salmonella-positive RTE chicken product, Line 2, 2026-08-10), and the underlying implementations (`single_agent/agent.py`, `multi_agent/graph.py`).

## Architecture difference

- **Single agent:** one LLM call, given all three data sources (sanitation logs, supplier records, process logs) at once.
- **Multi-agent:** three specialist agents run in parallel, each given only *one* data source, producing independent hypotheses. A fourth `cross_reference` node then re-evaluates each specialist's hypothesis against the sources it didn't see and synthesizes a final report.

## Result on this run

Both approaches converged on the **same root cause**: a CCP1 cook-step lethality deviation (07:30, 158°F/9min vs required 165°F/12min, no corrective action) combined with a skipped slicer changeover clean (11:50) enabling cross-contamination, with inadequate supplier COA sampling as a contributing factor. Both rated confidence **HIGH**.

## Advantages of multi-agent (observed)

- **Explicit blind-spot exposure.** Each specialist's hypothesis is checked against the data it didn't see, and the report explicitly flags what was "REVEALED" by that cross-check — creating a clear audit trail of what each specialist got right, wrong, or missed.
- **Hypothesis diversity before convergence.** Three independent first-pass theories exist before synthesis, reducing risk of anchoring on the first plausible cause (more valuable as source count/complexity grows).
- **Per-claim provenance.** Every finding is tagged with which specialist's "own data" vs. "blind to" data it came from — useful for audit/compliance contexts.
- **Scales better with more/larger sources:** avoids single-context-window overload, parallelizes latency, and allows source-specific specialization.

## Advantages of single-agent (observed)

- **Same conclusion, far cheaper.** One LLM call vs. four (3 parallel + 1 synthesis), with no material difference in accuracy or confidence for this dataset size (3 sources).
- **Lower latency and complexity** for small numbers of data sources.

## When multi-agent starts to matter more

- Context window pressure from many/large sources (10+ logs, large files) that a single agent would need to truncate or summarize lossily.
- Heterogeneous source formats benefiting from source-specific extraction/prompting.
- Higher risk of a single linear pass under-weighting a secondary/independent causal pathway.
- Need for parallel wall-clock speed across many sources.

## Caveat

As source count grows, the multi-agent `cross_reference`/synthesis step becomes the new bottleneck and may itself need to become hierarchical/multi-stage rather than a single flat reconciliation call.
