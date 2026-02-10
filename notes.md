# Notes and Design Decisions

## Why page-based processing
Research gaps often appear in specific sections or discussions.
Page-level metadata improves traceability and reduces hallucination risk.

## Why local LLM (Ollama)
- No data leakage
- No API dependency
- Deterministic testing
- Suitable for research workflows

## Why constrained prompting
Unconstrained generation leads to:
- fabricated gaps
- overly broad questions
- false confidence

This tool intentionally forces refusal when evidence is insufficient.

## Known limitations
- Signal detection is rule-based and conservative
- Questions may still require human refinement
- CPU-only inference is slow but acceptable for v0

## Future considerations (not implemented)
- Signal scoring and ranking
- Cross-paper contradiction detection
- Batch inference with persistent LLM sessions



### V1 Scope
- Improve evidence signal quality
- Reduce generic unanswered questions
- Preserve v0 behavior and outputs
