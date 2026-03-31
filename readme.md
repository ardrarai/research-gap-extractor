# Research Gap Extractor
**Status:** Experimental, Evidence-Grounded System

---

## 1. Problem

Understanding research literature is not primarily about summarizing what is known. The harder problem is identifying what remains unresolved.

Most LLM-based tools generate fluent summaries, but in doing so, they often obscure uncertainty, limitations, and missing evidence.

This system focuses on the opposite objective:

> Identify where the literature explicitly does not make claims.

---

## 2. Approach

Instead of summarizing content, the system:

- detects signals of uncertainty and limitation
- isolates those signals
- generates research questions only when supported by evidence

If no valid signal exists, the system refuses generation.

---

## 3. Pipeline
PDF → Page Extraction → Signal Detection → Constrained LLM → Structured Output

---

## 4. Signal Detection

The system identifies sentences containing:

- explicit limitations
- uncertainty
- missing evaluation
- unresolved claims

These signals are the only valid inputs for generation.

---

## 5. Output Structure

Each extracted gap is structured as:

| Field | Purpose |
|------|--------|
| QUESTION | Derived research gap |
| WHY | Evidence-based justification |
| MISSING | Missing data or evaluation |
| SOURCE | Paper and page reference |

---

## 6. System Behavior

| Condition | Output Behavior |
|----------|----------------|
| Strong signal present | Generates grounded research question |
| Weak signal | Conservative output |
| No signal | Refuses generation |

---

## 7. Evaluation Setup (v2)

The system was evaluated using:

- Semantic similarity (MiniLM embeddings)
- Precision@1
- Jaccard similarity
- Baseline heuristic comparison

---

## 8. Evaluation Results

| Metric | LLM System | Baseline |
|--------|------------|----------|
| Exact Match | 0.000 | 0.000 |
| Jaccard Similarity | 0.079 | 0.220 |
| Semantic Similarity | 0.757 | 0.705 |
| Semantic Match Rate | 0.667 | 0.333 |
| Precision@1 | 0.667 | 0.333 |

---

## 9. Interpretation

- Exact match is not meaningful for generative systems
- Semantic similarity better reflects alignment
- The LLM system shows higher precision than heuristic baseline
- Grounded generation improves relevance but reduces coverage

---

## 10. Failure Modes

- Misses implicit gaps not explicitly stated
- Conservative behavior may under-extract valid gaps
- Heuristic signal detection limits recall
- Domain generalization is limited

---

## 11. Setup

Install dependency:

```bash
pip install pdfplumber
```

---

Install local model:
```bash
ollama pull phi3:mini
```

---

## 12. Usage

Place PDF files in directory:
```bash
python -m cli.main --papers paper1.pdf paper2.pdf paper3.pdf
```

---

## 13. Design Decisions
- Generation is conditioned only on signal-bearing text
- One question per signal for traceability
- Refusal is enforced to prevent hallucination
- No external APIs used

---

## 14. Limitations
| Area       | Limitation               |
| ---------- | ------------------------ |
| Signals    | Keyword-based detection  |
| Dataset    | Small evaluation set     |
| Reasoning  | No cross-paper synthesis |
| Validation | No statistical testing   |

---

## 15. Design Philosophy
- Restraint over creativity
- Traceability over fluency
- Refusal over speculation

---

## 16. Purpose

This system is not designed to generate insights.

It is designed to reveal where insights cannot yet be made.
