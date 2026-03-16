#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from pathlib import Path
from typing import Dict, Tuple

import yaml
from deep_translator import GoogleTranslator


ZH_SECTION = "中文"
EN_SECTION = "English"
ZH_TITLE_KEY = "标题"
EN_TITLE_KEY = "title"


def first_meta_file(entry_dir: Path) -> Path | None:
    files = sorted(entry_dir.glob("meta_*.yaml"))
    return files[0] if files else None


def load_yaml(path: Path) -> Dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def save_yaml(path: Path, data: Dict) -> None:
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def sanitize_chinese_suffix(title: str, max_chars: int = 24) -> str:
    text = unicodedata.normalize("NFKC", title or "")
    text = text.strip()
    text = text.replace(" ", "")

    text = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "", text)
    text = re.sub(r"[，。、《》：；“”‘’（）()【】\[\]{}!,.?;:+*=~`@#$%^&·…、]", "", text)
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"-{2,}", "-", text)
    text = text.strip("-. _")

    if not text:
        text = "中文标题"
    if len(text) > max_chars:
        text = text[:max_chars].rstrip("-. _")
    return text or "中文标题"


def english_slug_prefix(dirname: str) -> str:
    if "__" in dirname:
        return dirname.split("__", 1)[0]
    return dirname


def ensure_unique_path(parent: Path, base_name: str) -> Path:
    target = parent / base_name
    if not target.exists():
        return target
    i = 2
    while True:
        candidate = parent / f"{base_name}-{i}"
        if not candidate.exists():
            return candidate
        i += 1


def update_index_csv(index_path: Path, name_map: Dict[str, str]) -> int:
    if not index_path.exists():
        return 0

    with index_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []

    if not rows or "slug" not in fieldnames:
        return 0

    changed = 0
    for row in rows:
        old_slug = row.get("slug", "")
        if old_slug in name_map:
            row["slug"] = name_map[old_slug]
            changed += 1

    if changed:
        with index_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    return changed


def translate_titles_and_rename(entries_root: Path, dry_run: bool) -> Tuple[int, int, int, int]:
    translator = GoogleTranslator(source="en", target="zh-CN")
    cache: Dict[str, str] = {}

    entries = sorted(
        p for p in entries_root.iterdir() if p.is_dir() and (p / "paper.pdf").exists()
    )
    translated = 0
    meta_updated = 0
    renamed = 0
    name_map: Dict[str, str] = {}

    for entry in entries:
        old_name = entry.name
        prefix = english_slug_prefix(old_name)

        meta = first_meta_file(entry)
        if meta is None:
            continue
        data = load_yaml(meta)

        en = data.get(EN_SECTION, {}) if isinstance(data.get(EN_SECTION), dict) else {}
        zh = data.get(ZH_SECTION, {}) if isinstance(data.get(ZH_SECTION), dict) else {}

        en_title = str(en.get(EN_TITLE_KEY) or "").strip()
        zh_title = str(zh.get(ZH_TITLE_KEY) or "").strip()

        if (not zh_title or zh_title == "NOT_SPECIFIED") and en_title:
            if en_title not in cache:
                try:
                    cache[en_title] = translator.translate(en_title)
                except Exception:
                    cache[en_title] = "中文标题"
            zh_title = cache[en_title].strip() or "中文标题"
            zh[ZH_TITLE_KEY] = zh_title
            data[ZH_SECTION] = zh
            translated += 1
            if not dry_run:
                save_yaml(meta, data)
            meta_updated += 1

        suffix = sanitize_chinese_suffix(zh_title)
        target_name = f"{prefix}__{suffix}"

        if old_name != target_name:
            target_path = ensure_unique_path(entry.parent, target_name)
            name_map[old_name] = target_path.name
            if not dry_run:
                entry.rename(target_path)
            renamed += 1

    index_changed = 0
    if not dry_run and renamed:
        index_changed = update_index_csv(entries_root / "index.csv", name_map)

    return translated, meta_updated, renamed, index_changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rename entry directories to english-slug__ChineseTitle suffix format."
    )
    parser.add_argument(
        "--entries-root",
        type=Path,
        default=Path("entries/cvpr2024"),
        help="Entries root directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview only, do not write files.",
    )
    args = parser.parse_args()

    if not args.entries_root.exists():
        print(f"[ERROR] entries root not found: {args.entries_root}")
        return 2

    translated, meta_updated, renamed, index_changed = translate_titles_and_rename(
        args.entries_root, args.dry_run
    )

    print(f"translated_titles: {translated}")
    print(f"meta_files_updated: {meta_updated}")
    print(f"renamed_dirs: {renamed}")
    print(f"index_rows_updated: {index_changed}")
    print(f"dry_run: {args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
