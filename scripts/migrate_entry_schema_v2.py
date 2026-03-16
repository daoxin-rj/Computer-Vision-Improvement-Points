#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

import yaml


LEGACY_TO_NEW_MD = {
    "beginner.md": "beginner_L1小白.md",
    "master.md": "master_L2入门.md",
    "research.md": "research_L3复现.md",
}

LEGACY_META = "meta.yaml"
LEGACY_IDEA = "idea.yaml"
NEW_META = "meta_元信息.yaml"
NEW_IDEA = "idea_改进点.yaml"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def write_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def pick(src: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in src:
            value = src[key]
            if value is not None and value != "":
                return value
    return default


def normalize_meta(
    legacy_meta: Dict[str, Any], current_meta: Dict[str, Any]
) -> Dict[str, Dict[str, Any]]:
    legacy_en = current_meta.get("English", {}) if isinstance(current_meta.get("English"), dict) else {}
    legacy_zh = current_meta.get("中文", {}) if isinstance(current_meta.get("中文"), dict) else {}

    en: Dict[str, Any] = {
        "title": pick(legacy_en, "title", default=pick(legacy_meta, "title", default=None)),
        "authors": pick(legacy_en, "authors", default=pick(legacy_meta, "authors", default=[])),
        "venue": pick(legacy_en, "venue", default=pick(legacy_meta, "venue", default=None)),
        "year": pick(legacy_en, "year", default=pick(legacy_meta, "year", default=None)),
        "url": pick(legacy_en, "url", default=pick(legacy_meta, "url", default=None)),
        "code_url": pick(legacy_en, "code_url", default=pick(legacy_meta, "code_url", default=None)),
        "field": pick(legacy_en, "field", default=pick(legacy_meta, "field", default=None)),
        "task": pick(legacy_en, "task", default=pick(legacy_meta, "task", default=None)),
        "summary_one_line": pick(
            legacy_en,
            "summary_one_line",
            default=pick(legacy_meta, "summary_one_line", default="NOT_SPECIFIED"),
        ),
    }

    zh: Dict[str, Any] = {
        "标题": pick(
            legacy_zh,
            "标题",
            default=pick(legacy_meta, "title_zh", default="NOT_SPECIFIED"),
        ),
        "作者": pick(
            legacy_zh,
            "作者",
            default=pick(legacy_meta, "authors_zh", "authors", default=[]),
        ),
        "会议": pick(
            legacy_zh,
            "会议",
            default=pick(legacy_meta, "venue_zh", "venue", default="NOT_SPECIFIED"),
        ),
        "年份": pick(
            legacy_zh,
            "年份",
            default=pick(legacy_meta, "year", default=None),
        ),
        "链接": pick(
            legacy_zh,
            "链接",
            default=pick(legacy_meta, "url", default=None),
        ),
        "代码链接": pick(
            legacy_zh,
            "代码链接",
            default=pick(legacy_meta, "code_url", default=None),
        ),
        "领域": pick(
            legacy_zh,
            "领域",
            default=pick(legacy_meta, "field_zh", default="NOT_SPECIFIED"),
        ),
        "任务": pick(
            legacy_zh,
            "任务",
            default=pick(legacy_meta, "task_zh", default="NOT_SPECIFIED"),
        ),
        "一句话总结": pick(
            legacy_zh,
            "一句话总结",
            default=pick(legacy_meta, "summary_one_line_zh", default="NOT_SPECIFIED"),
        ),
    }

    return {"English": en, "中文": zh}


def normalize_idea(
    legacy_idea: Dict[str, Any], current_idea: Dict[str, Any]
) -> Dict[str, Dict[str, Any]]:
    legacy_en = current_idea.get("English", {}) if isinstance(current_idea.get("English"), dict) else {}
    legacy_zh = current_idea.get("中文", {}) if isinstance(current_idea.get("中文"), dict) else {}

    en: Dict[str, Any] = {
        "improvement_point": pick(
            legacy_en, "improvement_point", default=pick(legacy_idea, "improvement_point", default=None)
        ),
        "core_mechanism": pick(
            legacy_en, "core_mechanism", default=pick(legacy_idea, "core_mechanism", default=None)
        ),
        "why_it_works": pick(
            legacy_en, "why_it_works", default=pick(legacy_idea, "why_it_works", default=None)
        ),
        "applicable_conditions": pick(
            legacy_en, "applicable_conditions", default=pick(legacy_idea, "applicable_conditions", default=[])
        ),
        "benefits": pick(legacy_en, "benefits", default=pick(legacy_idea, "benefits", default=[])),
        "tradeoffs": pick(legacy_en, "tradeoffs", default=pick(legacy_idea, "tradeoffs", default=[])),
        "transferability": pick(
            legacy_en, "transferability", default=pick(legacy_idea, "transferability", default=None)
        ),
        "implementation_hint": pick(
            legacy_en, "implementation_hint", default=pick(legacy_idea, "implementation_hint", default=None)
        ),
        "task_keywords": pick(
            legacy_en, "task_keywords", default=pick(legacy_idea, "task_keywords", default=[])
        ),
        "method_keywords": pick(
            legacy_en, "method_keywords", default=pick(legacy_idea, "method_keywords", default=[])
        ),
        "innovation_keywords": pick(
            legacy_en, "innovation_keywords", default=pick(legacy_idea, "innovation_keywords", default=[])
        ),
        "evidence_strength": pick(
            legacy_en, "evidence_strength", default=pick(legacy_idea, "evidence_strength", default=None)
        ),
        "reproducibility_confidence": pick(
            legacy_en,
            "reproducibility_confidence",
            default=pick(legacy_idea, "reproducibility_confidence", default=None),
        ),
        "novelty_confidence": pick(
            legacy_en, "novelty_confidence", default=pick(legacy_idea, "novelty_confidence", default=None)
        ),
    }

    zh: Dict[str, Any] = {
        "改进点": pick(
            legacy_zh,
            "改进点",
            default=pick(legacy_idea, "improvement_point_zh", default="NOT_SPECIFIED"),
        ),
        "核心机制": pick(
            legacy_zh,
            "核心机制",
            default=pick(legacy_idea, "core_mechanism_zh", default="NOT_SPECIFIED"),
        ),
        "有效原因": pick(
            legacy_zh,
            "有效原因",
            default=pick(legacy_idea, "why_it_works_zh", default="NOT_SPECIFIED"),
        ),
        "适用条件": pick(
            legacy_zh,
            "适用条件",
            default=pick(legacy_idea, "applicable_conditions_zh", default=[]),
        ),
        "收益": pick(legacy_zh, "收益", default=pick(legacy_idea, "benefits_zh", default=[])),
        "代价": pick(legacy_zh, "代价", default=pick(legacy_idea, "tradeoffs_zh", default=[])),
        "可迁移性": pick(
            legacy_zh,
            "可迁移性",
            default=pick(legacy_idea, "transferability_zh", default="NOT_SPECIFIED"),
        ),
        "实现提示": pick(
            legacy_zh,
            "实现提示",
            default=pick(legacy_idea, "implementation_hint_zh", default="NOT_SPECIFIED"),
        ),
        "任务关键词": pick(
            legacy_zh,
            "任务关键词",
            default=pick(legacy_idea, "task_keywords_zh", default=[]),
        ),
        "方法关键词": pick(
            legacy_zh,
            "方法关键词",
            default=pick(legacy_idea, "method_keywords_zh", default=[]),
        ),
        "创新关键词": pick(
            legacy_zh,
            "创新关键词",
            default=pick(legacy_idea, "innovation_keywords_zh", default=[]),
        ),
        "证据强度": pick(
            legacy_zh,
            "证据强度",
            default=pick(legacy_idea, "evidence_strength", default=None),
        ),
        "可复现性置信度": pick(
            legacy_zh,
            "可复现性置信度",
            default=pick(legacy_idea, "reproducibility_confidence", default=None),
        ),
        "创新性置信度": pick(
            legacy_zh,
            "创新性置信度",
            default=pick(legacy_idea, "novelty_confidence", default=None),
        ),
    }

    return {"English": en, "中文": zh}


def is_entry_dir(path: Path) -> bool:
    return path.is_dir() and (path / "paper.pdf").exists()


def migrate_entry(entry_dir: Path, templates: Dict[str, str], delete_legacy: bool) -> Dict[str, int]:
    counts = {"meta": 0, "idea": 0, "md": 0, "deleted": 0}

    legacy_meta = load_yaml(entry_dir / LEGACY_META)
    current_meta = load_yaml(entry_dir / NEW_META)
    new_meta = normalize_meta(legacy_meta, current_meta)
    write_yaml(entry_dir / NEW_META, new_meta)
    counts["meta"] += 1

    legacy_idea = load_yaml(entry_dir / LEGACY_IDEA)
    current_idea = load_yaml(entry_dir / NEW_IDEA)
    new_idea = normalize_idea(legacy_idea, current_idea)
    write_yaml(entry_dir / NEW_IDEA, new_idea)
    counts["idea"] += 1

    for legacy_name, new_name in LEGACY_TO_NEW_MD.items():
        legacy_path = entry_dir / legacy_name
        new_path = entry_dir / new_name

        if legacy_path.exists():
            content = read_text(legacy_path)
        elif new_path.exists():
            content = read_text(new_path)
        else:
            template_key = new_name
            content = templates[template_key]

        write_text(new_path, content)
        counts["md"] += 1

    if delete_legacy:
        for old_name in [LEGACY_META, LEGACY_IDEA, *LEGACY_TO_NEW_MD.keys()]:
            old_path = entry_dir / old_name
            if old_path.exists():
                old_path.unlink()
                counts["deleted"] += 1

    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate entries to bilingual filename/schema v2.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--entries-root", default="entries/cvpr2024")
    parser.add_argument("--keep-legacy", action="store_true", help="Do not delete legacy filenames.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    entries_root = (repo_root / args.entries_root).resolve()
    templates_root = repo_root / "templates"

    if not entries_root.exists():
        raise FileNotFoundError(f"Entries root not found: {entries_root}")
    if not templates_root.exists():
        raise FileNotFoundError(f"Templates root not found: {templates_root}")

    templates = {
        "beginner_L1小白.md": read_text(templates_root / "beginner_L1小白.md"),
        "master_L2入门.md": read_text(templates_root / "master_L2入门.md"),
        "research_L3复现.md": read_text(templates_root / "research_L3复现.md"),
    }

    total = 0
    stats = {"meta": 0, "idea": 0, "md": 0, "deleted": 0}
    for path in sorted(entries_root.rglob("*")):
        if not is_entry_dir(path):
            continue
        total += 1
        c = migrate_entry(path, templates, delete_legacy=not args.keep_legacy)
        for k, v in c.items():
            stats[k] += v

    print(f"Entries migrated: {total}")
    print(f"meta_元信息.yaml written: {stats['meta']}")
    print(f"idea_改进点.yaml written: {stats['idea']}")
    print(f"markdown files written: {stats['md']}")
    print(f"legacy files deleted: {stats['deleted']}")


if __name__ == "__main__":
    main()
