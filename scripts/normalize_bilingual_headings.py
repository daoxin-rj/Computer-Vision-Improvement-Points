#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, Tuple


HEADING_MAP: Dict[str, str] = {
    # L1 legacy headings
    "## 1. Problem": "## 1. Problem / 问题定义",
    "## 2. Why Old Methods Struggle": "## 2. Why Old Methods Struggle / 旧方法为何困难",
    "## 3. New Idea": "## 3. New Idea / 新方法核心想法",
    "## 4. Why It May Work Better": "## 4. Why It May Work Better / 为什么可能更有效",
    "## 5. Analogy": "## 5. Analogy / 直观类比",
    # L1 deep headings (english-only variant)
    "## 1. Background You Need First": "## 1. Background You Need First / 你需要先知道的背景",
    "## 2. Problem In One Sentence": "## 2. Problem In One Sentence / 一句话问题定义",
    "## 3. Why Existing Methods Struggle": "## 3. Why Existing Methods Struggle / 现有方法为什么会失败",
    "## 4. Method Walkthrough (Step-by-Step)": "## 4. Method Walkthrough (Step-by-Step) / 方法流程（分步讲解）",
    "## 5. Why This Design Makes Sense": "## 5. Why This Design Makes Sense / 为什么这个设计合理",
    "## 6. Mini Example Or Thought Experiment": "## 6. Mini Example Or Thought Experiment / 小例子或思维实验",
    "## 7. Learning Path For This Week": "## 7. Learning Path For This Week / 本周学习路径",
    "## 8. Common Confusions And Self-Check Questions": "## 8. Common Confusions And Self-Check Questions / 常见误区与自测问题",
    # L2 legacy headings
    "## 1. Task Definition": "## 1. Task Definition / 任务定义",
    "## 2. Baseline": "## 2. Baseline / 基线方法",
    "## 3. Core Innovation": "## 3. Core Innovation / 核心创新",
    "## 4. Method Modules": "## 4. Method Modules / 方法模块拆解",
    "## 5. Why Effective": "## 5. Why Effective / 为什么有效",
    "## 6. Experimental Evidence": "## 6. Experimental Evidence / 实验证据",
    # L2 deep headings (english-only variant)
    "## 1. Task Setup And Evaluation Target": "## 1. Task Setup And Evaluation Target / 任务设定与评估目标",
    "## 2. Baseline Family And Failure Analysis": "## 2. Baseline Family And Failure Analysis / 基线家族与失败分析",
    "## 3. Core Innovation And Positioning": "## 3. Core Innovation And Positioning / 核心创新与方法定位",
    "## 4. Module-Level Pipeline": "## 4. Module-Level Pipeline / 模块级流程拆解",
    "## 5. Design Rationale (Why Each Module Exists)": "## 5. Design Rationale (Why Each Module Exists) / 设计动机（每个模块为何存在）",
    "## 6. Training And Inference Details": "## 6. Training And Inference Details / 训练与推理细节",
    "## 7. Evidence Mapping (Claim -> Experiment)": "## 7. Evidence Mapping (Claim -> Experiment) / 证据映射（结论 -> 实验）",
    "## 8. Transferability And Limits": "## 8. Transferability And Limits / 可迁移性与边界",
    # L3 legacy headings
    "## 1. Problem Formulation": "## 1. Problem Formulation / 问题形式化",
    "## 2. Key Notation": "## 2. Key Notation / 关键符号",
    "## 3. Core Formulation": "## 3. Core Formulation / 核心公式",
    "## 4. Reasoning Or Derivation": "## 4. Reasoning Or Derivation / 推导与设计动机",
    "## 5. Algorithm Or Pipeline": "## 5. Algorithm Or Pipeline / 算法流程",
    "## 6. Training Strategy": "## 6. Training Strategy / 训练策略",
    "## 7. Inference Strategy": "## 7. Inference Strategy / 推理策略",
    "## 8. Ablation-Relevant Insights": "## 8. Ablation-Relevant Insights / 消融关键信息",
    "## 9. Reproduction Risks": "## 9. Reproduction Risks / 复现风险",
    # L3 deep headings (english-only variant)
    "## 1. Formal Problem Setup": "## 1. Formal Problem Setup / 形式化问题设定",
    "## 2. Notation And Data Representation": "## 2. Notation And Data Representation / 符号与数据表示",
    "## 3. Objective/Formulation": "## 3. Objective/Formulation / 目标函数与形式化表达",
    "## 4. Architecture And Information Flow": "## 4. Architecture And Information Flow / 架构与信息流",
    "## 5. End-to-End Algorithm": "## 5. End-to-End Algorithm / 端到端算法流程",
    "## 6. Training Recipe": "## 6. Training Recipe / 训练配方",
    "## 7. Inference Recipe": "## 7. Inference Recipe / 推理配方",
    "## 8. Ablation Logic": "## 8. Ablation Logic / 消融实验逻辑",
    "## 9. Reproduction Checklist": "## 9. Reproduction Checklist / 复现检查清单",
    "## 10. Failure Modes And Debug Order": "## 10. Failure Modes And Debug Order / 失败模式与调试顺序",
}


def iter_entry_markdown_files(entries_root: Path) -> Iterable[Path]:
    for entry in sorted(p for p in entries_root.iterdir() if p.is_dir()):
        if not (entry / "paper.pdf").exists():
            continue
        for pattern in ("beginner_L1*.md", "master_L2*.md", "research_L3*.md"):
            for md in sorted(entry.glob(pattern)):
                yield md


def normalize_file(path: Path) -> Tuple[bool, int]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    changed = False
    replacements = 0

    for i, line in enumerate(lines):
        replacement = HEADING_MAP.get(line.strip())
        if replacement and line != replacement:
            lines[i] = replacement
            changed = True
            replacements += 1

    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed, replacements


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize L1/L2/L3 markdown headings to EN/ZH bilingual format.")
    parser.add_argument(
        "--entries-root",
        type=Path,
        default=Path("entries/cvpr2024"),
        help="Root directory for entry folders.",
    )
    args = parser.parse_args()

    if not args.entries_root.exists():
        print(f"[ERROR] entries root not found: {args.entries_root}")
        return 2

    file_count = 0
    changed_files = 0
    replacement_count = 0

    for md in iter_entry_markdown_files(args.entries_root):
        file_count += 1
        changed, replacements = normalize_file(md)
        if changed:
            changed_files += 1
            replacement_count += replacements

    print(f"scanned_files: {file_count}")
    print(f"changed_files: {changed_files}")
    print(f"heading_replacements: {replacement_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
