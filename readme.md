# Research Gap Extractor

This is a personal research tool I built while working on an interdisciplinary paper, where I repeatedly ran into the same problem:

I could read papers, but I struggled to clearly see **what was still unanswered**, especially when comparing multiple papers across domains.

Instead of summarizing literature (which I found unhelpful), this tool focuses on extracting **unanswered research questions** by looking at where authors themselves express uncertainty, limitations, or incomplete evidence.

---

## Why I built this

When starting a paper from scratch, I faced a few recurring issues:

- Understanding terminology and context in an unfamiliar domain required reading many papers
- Comparing multiple papers was slow and mentally exhausting
- It was easy to forget where different papers disagreed or left things open
- Generic AI summaries hid research gaps instead of revealing them

I built this tool to help me **locate where the literature stops**, not where it feels confident.

---

## What this tool does

- Takes multiple academic papers as PDF files
- Extracts page-level text with metadata
- Detects explicit signals such as:
  - uncertainty
  - stated limitations
  - implicit assumptions
- Uses a constrained **local** language model to derive unanswered research questions
- Produces questions that are:
  - directly traceable to a paper and page
  - conservative and evidence-grounded
  - meant as starting points for further investigation, not final answers

---

## What this tool intentionally does NOT do

- It does not summarize papers
- It does not draw conclusions
- It does not propose solutions
- It does not invent gaps or speculate
- It does not use cloud APIs or external data

These are deliberate design decisions.
The goal is **clarity and honesty**, not completeness or speed.

---

## How it works (high level)

1. **Ingestion**
   - PDFs are loaded and split into pages
   - Text is cleaned while preserving structure

2. **Structuring**
   - Pages are chunked with metadata (paper, page, section)

3. **Evidence Detection**
   - Rule-based detection of uncertainty and limitation signals

4. **Question Extraction**
   - A local LLM is prompted under strict constraints
   - One unanswered question is derived per signal
   - The model is forced to refuse if no valid gap exists

---

## Requirements

- Python 3.9+
- Ollama (local LLM runtime)
- Tested on:
  - Windows
  - CPU-only environment

---

## Setup

Install the Python dependency:

```bash
pip install pdfplumber
```

Install and pull the local model:

```bash
ollama pull phi3:mini
```

## Usage

Place at least three PDF papers in the project directory, then run:

```bash
python -m cli.main --papers paper1.pdf paper2.pdf paper3.pdf
```

## OUTPUT

The tool outputs one or more unanswered research questions in the following structure:
QUESTION: <research question>

WHY: <why this question exists based on evidence>

MISSING: <what data or evaluation is absent>

Source:
Paper X — page Y (signal type)
Each question can be traced back to the exact location in the literature.

## Design philosophy

This project prioritizes:

- correctness over speed
- traceability over fluency
- restraint over creativity
- It is intentionally limited and conservative.

