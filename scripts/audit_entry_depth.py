#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


REQUIRED_SECTIONS: Dict[str, List[str]] = {
    "beginner": [
        "## 1. Background You Need First / 你需要先知道的背景",
        "## 2. Problem In One Sentence / 一句话问题定义",
        "## 3. Why Existing Methods Struggle / 现有方法为什么会失败",
        "## 4. Method Walkthrough (Step-by-Step) / 方法流程（分步讲解）",
        "## 5. Why This Design Makes Sense / 为什么这个设计合理",
        "## 6. Mini Example Or Thought Experiment / 小例子或思维实验",
        "## 7. Learning Path For This Week / 本周学习路径",
        "## 8. Common Confusions And Self-Check Questions / 常见误区与自测问题",
    ],
    "master": [
        "## 1. Task Setup And Evaluation Target / 任务设定与评估目标",
        "## 2. Baseline Family And Failure Analysis / 基线家族与失败分析",
        "## 3. Core Innovation And Positioning / 核心创新与方法定位",
        "## 4. Module-Level Pipeline / 模块级流程拆解",
        "## 5. Design Rationale (Why Each Module Exists) / 设计动机（每个模块为何存在）",
        "## 6. Training And Inference Details / 训练与推理细节",
        "## 7. Evidence Mapping (Claim -> Experiment) / 证据映射（结论 -> 实验）",
        "## 8. Transferability And Limits / 可迁移性与边界",
    ],
    "research": [
        "## 1. Formal Problem Setup / 形式化问题设定",
        "## 2. Notation And Data Representation / 符号与数据表示",
        "## 3. Objective/Formulation / 目标函数与形式化表达",
        "## 4. Architecture And Information Flow / 架构与信息流",
        "## 5. End-to-End Algorithm / 端到端算法流程",
        "## 6. Training Recipe / 训练配方",
        "## 7. Inference Recipe / 推理配方",
        "## 8. Ablation Logic / 消融实验逻辑",
        "## 9. Reproduction Checklist / 复现检查清单",
        "## 10. Failure Modes And Debug Order / 失败模式与调试顺序",
    ],
}

MIN_NONSPACE_CHARS = {
    "beginner": 1200,
    "master": 1800,
    "research": 2600,
}

FILE_PATTERNS = {
    "beginner": "beginner_L1*.md",
    "master": "master_L2*.md",
    "research": "research_L3*.md",
}


@dataclass
class FileIssue:
    entry: str
    file_path: str
    level: str
    issues: List[str]


def first_match(directory: Path, pattern: str) -> Path | None:
    matches = sorted(directory.glob(pattern))
    return matches[0] if matches else None


def nonspace_char_count(text: str) -> int:
    return sum(1 for ch in text if not ch.isspace())


def validate_markdown(path: Path, level: str) -> List[str]:
    issues: List[str] = []
    text = path.read_text(encoding="utf-8")

    for heading in REQUIRED_SECTIONS[level]:
        if heading not in text:
            issues.append(f"missing heading: {heading}")

    if "### EN" not in text or "### ZH" not in text:
        issues.append("missing bilingual markers (### EN / ### ZH)")

    chars = nonspace_char_count(text)
    if chars < MIN_NONSPACE_CHARS[level]:
        issues.append(
            f"too short: non-space chars={chars}, expected>={MIN_NONSPACE_CHARS[level]}"
        )

    not_specified_count = text.count("NOT_SPECIFIED")
    if not_specified_count > 6:
        issues.append(f"too many NOT_SPECIFIED placeholders: {not_specified_count}")

    return issues


def collect_entry_dirs(entries_root: Path) -> List[Path]:
    if entries_root.is_dir() and (entries_root / "paper.pdf").exists():
        return [entries_root]
    return sorted(
        p for p in entries_root.iterdir() if p.is_dir() and (p / "paper.pdf").exists()
    )


def audit_entries(entries_root: Path) -> Tuple[List[FileIssue], int]:
    entry_dirs = collect_entry_dirs(entries_root)
    file_issues: List[FileIssue] = []

    for entry in entry_dirs:
        for level, pattern in FILE_PATTERNS.items():
            md_path = first_match(entry, pattern)
            if md_path is None:
                file_issues.append(
                    FileIssue(
                        entry=entry.name,
                        file_path=str(entry),
                        level=level,
                        issues=[f"missing file pattern: {pattern}"],
                    )
                )
                continue

            issues = validate_markdown(md_path, level)
            if issues:
                file_issues.append(
                    FileIssue(
                        entry=entry.name,
                        file_path=str(md_path),
                        level=level,
                        issues=issues,
                    )
                )

    return file_issues, len(entry_dirs)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit L1/L2/L3 depth quality for repository entries."
    )
    parser.add_argument(
        "--entries-root",
        type=Path,
        default=Path("entries/cvpr2024"),
        help="Root directory containing entry folders.",
    )
    parser.add_argument(
        "--max-report",
        type=int,
        default=40,
        help="Maximum number of failing files to print in detail.",
    )
    parser.add_argument(
        "--fail-on-issue",
        action="store_true",
        help="Return exit code 1 if any issue is found.",
    )
    args = parser.parse_args()

    if not args.entries_root.exists():
        print(f"[ERROR] entries root not found: {args.entries_root}")
        return 2

    issues, total_entries = audit_entries(args.entries_root)

    if not issues:
        print(f"[OK] audited {total_entries} entries, no depth issues found.")
        return 0

    print(
        f"[WARN] audited {total_entries} entries, found {len(issues)} files with depth issues."
    )

    for item in issues[: args.max_report]:
        print(f"\n[{item.level}] {item.entry}")
        print(f"file: {item.file_path}")
        for issue in item.issues:
            print(f"- {issue}")

    if len(issues) > args.max_report:
        print(f"\n... truncated {len(issues) - args.max_report} additional issue records ...")

    return 1 if args.fail_on_issue else 0


if __name__ == "__main__":
    raise SystemExit(main())
