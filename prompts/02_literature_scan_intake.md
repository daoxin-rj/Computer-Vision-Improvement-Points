# Prompt 02: Literature Scan And Intake Candidates

You are responsible for novelty scan and candidate intake.

Inputs:
- topic: {{topic}}
- time_range: {{time_range}}

Selection policy:
1. Prefer papers with explicit method improvements.
2. Exclude pure surveys, pure benchmark-only papers, and pure resource papers.
3. Prioritize clear mechanism, transferability, and sufficient empirical evidence.
4. Cluster papers sharing the same mechanism family.
5. Do not overrate simple backbone/dataset swaps unless mechanism is truly reusable.

Per-paper output fields:
- title
- year
- venue_or_arxiv
- topic_fit
- main_problem
- main_method
- key_improvement
- evidence_strength
- add_priority (high|medium|low)
- duplicate_risk
- next_action (add|compare|skip)

Final summary:
1. Top-N recommended papers for intake
2. Most reusable improvement point for each
3. Overlap risks with current repository direction

