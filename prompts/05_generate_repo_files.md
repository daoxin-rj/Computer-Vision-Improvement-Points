# Prompt 05: Generate Repository Files

Generate only the file contents for these five files:
1. meta_元信息.yaml
2. beginner_L1小白.md
3. master_L2入门.md
4. research_L3复现.md
5. idea_改进点.yaml

Rules:
1. Keep field names fixed.
2. Keep style consistent across files.
3. Use `null` or `NOT_SPECIFIED` for missing information.
4. Do not output extra explanation outside file contents.
5. For markdown and text fields, write English first and then provide Chinese translation.
6. For YAML files, use top-level sections `English` and `中文`.
7. Chinese section must use Chinese key names instead of `_zh` suffix keys.
8. L1/L2/L3 must be detailed enough for learning and implementation planning; avoid short abstract-like outputs.

Mandatory markdown depth structure:

beginner_L1小白.md must include these sections:
- 1) Background You Need First
- 2) Problem In One Sentence
- 3) Why Existing Methods Struggle
- 4) Method Walkthrough (Step-by-Step)
- 5) Why This Design Makes Sense
- 6) Mini Example Or Thought Experiment
- 7) Learning Path For This Week
- 8) Common Confusions And Self-Check Questions

master_L2入门.md must include these sections:
- 1) Task Setup And Evaluation Target
- 2) Baseline Family And Failure Analysis
- 3) Core Innovation And Positioning
- 4) Module-Level Pipeline
- 5) Design Rationale (Why Each Module Exists)
- 6) Training And Inference Details
- 7) Evidence Mapping (Claim -> Experiment)
- 8) Transferability And Limits

research_L3复现.md must include these sections:
- 1) Formal Problem Setup
- 2) Notation And Data Representation
- 3) Objective/Formulation
- 4) Architecture And Information Flow
- 5) End-to-End Algorithm
- 6) Training Recipe
- 7) Inference Recipe
- 8) Ablation Logic
- 9) Reproduction Checklist
- 10) Failure Modes And Debug Order

Depth minimum:
- L1: at least 8 non-trivial bullets/sentences in EN and mirrored in ZH.
- L2: include explicit claim-to-evidence mapping (at least 3 mappings).
- L3: include explicit reproduction checklist (at least 8 checklist items).

Required field schema:

meta_元信息.yaml
- English.title
- English.authors
- English.venue
- English.year
- English.url
- English.code_url
- English.field
- English.task
- English.summary_one_line
- 中文.标题
- 中文.作者
- 中文.会议
- 中文.年份
- 中文.链接
- 中文.代码链接
- 中文.领域
- 中文.任务
- 中文.一句话总结

idea_改进点.yaml
- English.improvement_point
- English.core_mechanism
- English.why_it_works
- English.applicable_conditions
- English.benefits
- English.tradeoffs
- English.transferability
- English.implementation_hint
- English.task_keywords
- English.method_keywords
- English.innovation_keywords
- English.evidence_strength
- English.reproducibility_confidence
- English.novelty_confidence
- 中文.改进点
- 中文.核心机制
- 中文.有效原因
- 中文.适用条件
- 中文.收益
- 中文.代价
- 中文.可迁移性
- 中文.实现提示
- 中文.任务关键词
- 中文.方法关键词
- 中文.创新关键词
- 中文.证据强度
- 中文.可复现性置信度
- 中文.创新性置信度
