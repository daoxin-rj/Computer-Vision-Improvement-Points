# Prompt 05: Generate Repository Files

Generate only the file contents for these five files:
1. meta.yaml
2. beginner.md
3. master.md
4. research.md
5. idea.yaml

Rules:
1. Keep field names fixed.
2. Keep style consistent across files.
3. Use `null` or `NOT_SPECIFIED` for missing information.
4. Do not output extra explanation outside file contents.
5. For markdown and text fields, write English first and then provide Chinese translation.

Required field schema:

meta.yaml
- title
- authors
- venue
- year
- url
- code_url
- field
- task
- summary_one_line

idea.yaml
- improvement_point
- core_mechanism
- why_it_works
- applicable_conditions
- benefits
- tradeoffs
- transferability
- implementation_hint
- task_keywords
- method_keywords
- innovation_keywords
- evidence_strength
- reproducibility_confidence
- novelty_confidence
