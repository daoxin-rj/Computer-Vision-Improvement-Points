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
- 1) Background You Need First / 你需要先知道的背景
- 2) Problem In One Sentence / 一句话问题定义
- 3) Why Existing Methods Struggle / 现有方法为什么会失败
- 4) Method Walkthrough (Step-by-Step) / 方法流程（分步讲解）
- 5) Why This Design Makes Sense / 为什么这个设计合理
- 6) Mini Example Or Thought Experiment / 小例子或思维实验
- 7) Learning Path For This Week / 本周学习路径
- 8) Common Confusions And Self-Check Questions / 常见误区与自测问题

master_L2入门.md must include these sections:
- 1) Task Setup And Evaluation Target / 任务设定与评估目标
- 2) Baseline Family And Failure Analysis / 基线家族与失败分析
- 3) Core Innovation And Positioning / 核心创新与方法定位
- 4) Module-Level Pipeline / 模块级流程拆解
- 5) Design Rationale (Why Each Module Exists) / 设计动机（每个模块为何存在）
- 6) Training And Inference Details / 训练与推理细节
- 7) Evidence Mapping (Claim -> Experiment) / 证据映射（结论 -> 实验）
- 8) Transferability And Limits / 可迁移性与边界

research_L3复现.md must include these sections:
- 1) Formal Problem Setup / 形式化问题设定
- 2) Notation And Data Representation / 符号与数据表示
- 3) Objective/Formulation / 目标函数与形式化表达
- 4) Architecture And Information Flow / 架构与信息流
- 5) End-to-End Algorithm / 端到端算法流程
- 6) Training Recipe / 训练配方
- 7) Inference Recipe / 推理配方
- 8) Ablation Logic / 消融实验逻辑
- 9) Reproduction Checklist / 复现检查清单
- 10) Failure Modes And Debug Order / 失败模式与调试顺序

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
