A. Research Gap Extraction Pipeline (your flagship)

This project is already strong. Don’t expand scope. Deepen it.

What to achieve next (pick 2–3, not all)
1. Cross-document behavior (HIGH VALUE)

Right now it’s mostly single-document focused.

Add this experiment:

Run the pipeline on 2–3 papers in the same domain

Observe:

Do gaps repeat?

Do gaps contradict?

Does retrieval depth amplify noise?

Document findings:

“Increasing retrieval depth across multiple papers increases conceptual breadth but also introduces redundancy.”

This is research insight, not engineering.

2. Stability test (VERY RARE at student level)

Do this:

Fix one configuration

Run the pipeline 3–5 times

Compare:

Gap overlap

Semantic similarity between runs

If results vary, say so.

That gives you a powerful line:

“Observed variance in generative outputs under identical configurations, highlighting stability as an unresolved challenge.”

Most people avoid this. Researchers respect it.

3. Explicit failure cases section (DO THIS)

Create a small markdown file or README section:

When does the system:

Miss obvious gaps?

Over-extract trivial limitations?

Refuse too often?

This turns your project from demo → study.

🎯 Outcome you want from this project

When asked:

“What did you learn?”

You should answer:

“That chunking and retrieval depth dominate reasoning behavior more than model choice, and stability is still an open problem.”

That’s an extraordinary answer.
