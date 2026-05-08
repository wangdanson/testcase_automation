#!/usr/bin/env python3
"""Orchestrate Confluence sync and print a spec knowledge update handoff."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_ROOTS = ("source_files", "user_manual")
SPEC_ROOT = "spec_knowledge"
SYNC_SCRIPT = "sync_from_confluence.py"

SYSTEM_PATTERNS = {
    "SuperDSP": ("SuperDSP", "Commerce AD", "AOE", "CCT", "Custom Audience", "FlashDrive"),
    "ODM": ("ODM", "委刊單", "RMN", "Cue", "Placement", "TextDrive", "SudoPlacement"),
    "OSS/ERP": ("OSS", "ERP", "合約", "帳務", "接單公司", "媒體格式設定"),
    "OYM": ("OYM", "媒體端", "底價", "floor price"),
    "Studio": ("Studio", "STUDIO", "素材管理", "素材包"),
}

SYSTEM_DESTINATIONS = {
    "SuperDSP": ("spec_knowledge/SuperDSP_RULES.md", "spec_knowledge/SYSTEM_MAP.md"),
    "ODM": ("spec_knowledge/ODM_REPORT_TRACKING.md", "spec_knowledge/SYSTEM_MAP.md"),
    "OSS/ERP": ("spec_knowledge/OSS_RULES.md", "spec_knowledge/ERP_RULES.md", "spec_knowledge/SYSTEM_MAP.md"),
    "OYM": ("spec_knowledge/OYM_RULES.md", "spec_knowledge/SYSTEM_MAP.md"),
    "Studio": ("spec_knowledge/STUDIO_RULES.md", "spec_knowledge/SYSTEM_MAP.md"),
    "Unclassified": ("spec_knowledge/SYSTEM_MAP.md",),
}

FILE_LABELS = {
    ".html": "HTML",
    ".md": "MD",
    ".csv": "CSV",
    ".xlsx": "XLSX",
    ".xls": "XLS",
    ".png": "IMG",
    ".jpg": "IMG",
    ".jpeg": "IMG",
    ".mmd": "MMD",
    ".drawio": "DRAWIO",
    ".json": "JSON",
    ".eml": "EML",
}


class Style:
    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    def paint(self, text: str, code: str) -> str:
        if not self.enabled:
            return text
        return f"\033[{code}m{text}\033[0m"

    def title(self, text: str) -> str:
        return self.paint(text, "1;36")

    def section(self, text: str) -> str:
        return self.paint(text, "1;34")

    def add(self, text: str) -> str:
        return self.paint(text, "32")

    def change(self, text: str) -> str:
        return self.paint(text, "33")

    def remove(self, text: str) -> str:
        return self.paint(text, "31")

    def warn(self, text: str) -> str:
        return self.paint(text, "33")

    def muted(self, text: str) -> str:
        return self.paint(text, "2")

    def path(self, text: str) -> str:
        return self.paint(text, "36")

    def system(self, text: str) -> str:
        return self.paint(text, "1;35")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run Confluence sync, detect changed spec sources, and create an AI "
            "handoff summary for spec_knowledge updates."
        )
    )
    parser.add_argument(
        "--no-sync",
        action="store_true",
        help="Do not run sync_from_confluence.py; only create a report from current workspace state.",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=80,
        help="Maximum changed source files to include directly in the handoff prompt.",
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Also write JSON/Markdown handoff files under .sync_reports/.",
    )
    parser.add_argument(
        "--view",
        choices=("grouped", "flat", "summary"),
        default="grouped",
        help="Terminal output style.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colors in terminal output.",
    )
    return parser.parse_args()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return "__pycache__" in parts or path.name in {".DS_Store", "Thumbs.db"}


def iter_files(root_names: tuple[str, ...] | list[str]):
    for root_name in root_names:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and not should_skip(path):
                yield path


def snapshot(root_names: tuple[str, ...] | list[str]) -> dict[str, dict[str, int | str]]:
    result: dict[str, dict[str, int | str]] = {}
    for path in iter_files(root_names):
        stat = path.stat()
        result[rel(path)] = {
            "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
            "suffix": path.suffix.lower(),
        }
    return result


def diff_snapshots(
    before: dict[str, dict[str, int | str]], after: dict[str, dict[str, int | str]]
) -> dict[str, list[str]]:
    before_keys = set(before)
    after_keys = set(after)
    added = sorted(after_keys - before_keys)
    removed = sorted(before_keys - after_keys)
    modified = sorted(
        key
        for key in before_keys & after_keys
        if before[key]["size"] != after[key]["size"]
        or before[key]["mtime_ns"] != after[key]["mtime_ns"]
    )
    return {"added": added, "modified": modified, "removed": removed}


def run_sync_script() -> tuple[int, list[str]]:
    command = [sys.executable, SYNC_SCRIPT]
    print(f"[sync-knowledge] Running: {' '.join(command)}")
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    output: list[str] = []
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="")
        output.append(line.rstrip("\n"))

    return process.wait(), output


def git_status(paths: tuple[str, ...] | list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-c", "core.quotePath=false", "status", "--short", "--", *paths],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def classify_path(path: str) -> str:
    for system, keywords in SYSTEM_PATTERNS.items():
        if any(keyword.lower() in path.lower() for keyword in keywords):
            return system
    return "Unclassified"


def classify_paths(paths: list[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for path in paths:
        result.setdefault(classify_path(path), []).append(path)
    return result


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def render_list(items: list[str], limit: int | None = None) -> str:
    selected = items if limit is None else items[:limit]
    if not selected:
        return "- 無"
    lines = [f"- `{item}`" for item in selected]
    if limit is not None and len(items) > limit:
        lines.append(f"- ... 還有 {len(items) - limit} 個項目，請用 `--max-files` 提高顯示上限")
    return "\n".join(lines)


def file_label(path: str) -> str:
    suffix = Path(path).suffix.lower()
    return FILE_LABELS.get(suffix, "FILE")


def group_key(path: str) -> str:
    parts = Path(path).parts
    if len(parts) <= 2:
        return path
    return "/".join(parts[:2])


def group_paths(paths: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for path in sorted(paths):
        groups.setdefault(group_key(path), []).append(path)
    return groups


def format_grouped_paths(
    title: str,
    paths: list[str],
    style: Style,
    max_groups: int,
    max_files_per_group: int = 8,
) -> str:
    lines = [style.section(title)]
    if not paths:
        lines.append(f"  {style.muted('無')}")
        return "\n".join(lines)

    groups = group_paths(paths)
    for index, (group, group_items) in enumerate(groups.items()):
        if index >= max_groups:
            lines.append(
                f"  {style.warn('…')} 還有 {len(groups) - max_groups} 個群組，請用 `--max-files` 提高顯示上限"
            )
            break

        system = classify_path(group)
        destinations = ", ".join(SYSTEM_DESTINATIONS.get(system, SYSTEM_DESTINATIONS["Unclassified"]))
        lines.append(f"\n  {style.path(group)}")
        lines.append(f"     系統: {style.system(system)}")
        lines.append(f"     落點: {style.path(destinations)}")
        lines.append("     檔案:")

        for file_index, item in enumerate(group_items):
            if file_index >= max_files_per_group:
                lines.append(f"       {style.warn('…')} 還有 {len(group_items) - max_files_per_group} 個檔案")
                break
            display_name = Path(item).name
            lines.append(f"       [{file_label(item)}] {display_name}")

    return "\n".join(lines)


def format_flat_paths(title: str, paths: list[str], style: Style, limit: int) -> str:
    lines = [style.section(title)]
    if not paths:
        lines.append(f"  {style.muted('無')}")
        return "\n".join(lines)
    for item in paths[:limit]:
        lines.append(f"  [{file_label(item)}] {style.path(item)}")
    if len(paths) > limit:
        lines.append(f"  {style.warn('…')} 還有 {len(paths) - limit} 個項目，請用 `--max-files` 提高顯示上限")
    return "\n".join(lines)


def build_terminal_summary(report: dict, max_files: int, view: str, style: Style) -> str:
    source_diff = report["source_diff"]
    changed_sources = source_diff["added"] + source_diff["modified"]
    source_git_status = [
        line
        for line in report["git_status"]
        if "source_files/" in line or "user_manual/" in line
    ]
    spec_git_status = [line for line in report["git_status"] if "spec_knowledge/" in line]
    lines = [
        "",
        style.title("規格知識庫同步結果"),
        "",
        f"執行時間: {report['created_at']}",
        f"同步腳本: {SYNC_SCRIPT}",
        f"已執行 Confluence 同步: {report['sync_executed']}",
        f"同步結束碼: {report['sync_exit_code']}",
        "",
        style.section("變更摘要"),
        f"  新增來源檔案: {style.add(str(len(source_diff['added'])))}",
        f"  修改來源檔案: {style.change(str(len(source_diff['modified'])))}",
        f"  移除來源檔案: {style.remove(str(len(source_diff['removed'])))}",
        f"  影響系統: {', '.join(report['candidate_systems'].keys()) or '無'}",
        "",
    ]

    if view == "summary":
        lines.append(style.muted("📋 已使用 summary view，略過檔案明細。"))
    elif view == "flat":
        lines.extend(
            [
                format_flat_paths("🟢 新增", source_diff["added"], style, max_files),
                "",
                format_flat_paths("🟡 修改", source_diff["modified"], style, max_files),
                "",
                format_flat_paths("🔴 移除", source_diff["removed"], style, max_files),
            ]
        )
    else:
        lines.extend(
            [
                format_grouped_paths("🟢 新增規格群組", source_diff["added"], style, max_files),
                "",
                format_grouped_paths("🟡 修改規格群組", source_diff["modified"], style, max_files),
                "",
                format_grouped_paths("🔴 移除規格群組", source_diff["removed"], style, max_files),
            ]
        )

    lines.extend(
        [
            "",
            style.section("候選系統分類"),
            json.dumps(report["candidate_systems"], ensure_ascii=False, indent=2) or "{}",
            "",
            style.section("來源檔案 Git 狀態"),
            render_list(source_git_status, max_files),
            "",
            style.section("spec_knowledge Git 狀態"),
            render_list(spec_git_status, max_files),
            "",
            style.section("下一步"),
            f"- 分析 `{SOURCE_ROOTS[0]}/` 與 `{SOURCE_ROOTS[1]}/` 的新增/修改規格內容。",
            "- 更新或新增 `spec_knowledge/*.md`。",
            "- 必須同步更新 `spec_knowledge/SYSTEM_MAP.md`。",
            "- 若圖片、drawio、mmd、csv 尚未解析，完成時列為待確認風險。",
            "",
        ]
    )

    return "\n".join(lines)


def build_markdown_report(report: dict, max_files: int) -> str:
    return "# Sync Knowledge Report\n" + build_terminal_summary(report, max_files, "grouped", Style(False))


def build_handoff_prompt(report: dict, max_files: int) -> str:
    source_diff = report["source_diff"]
    changed_sources = source_diff["added"] + source_diff["modified"]
    candidate_systems = report["candidate_systems"]
    spec_docs = report["spec_docs"]

    return f"""# Spec Knowledge Update Handoff

請使用繁體中文處理本任務。

## 目標
根據本次 Confluence 同步後的新增/修改規格，分析可重用的 QA / 業務規則，更新或新增 `spec_knowledge/*.md`，並同步更新 `spec_knowledge/SYSTEM_MAP.md`。

## 報告來源
- Sync executed: `{report["sync_executed"]}`
- Sync exit code: `{report["sync_exit_code"]}`

## 本次新增/修改來源檔案
{render_list(changed_sources, max_files)}

## 候選系統分類
```json
{json.dumps(candidate_systems, ensure_ascii=False, indent=2)}
```

## 目前知識庫文件
{render_list(spec_docs, None)}

## 必做流程
1. 先讀取現有 `spec_knowledge/` 文件，嚴禁盲寫覆蓋。
2. 逐一分析本次新增/修改的 `source_files/` 或 `user_manual/` 內容。
3. 不只依資料夾名稱分類；若資料夾未包含 ODM / SuperDSP / OSS / ERP / OYM / Studio，仍需依內容判斷歸屬。
4. 若屬於既有系統，更新對應知識文件，例如 `SuperDSP_RULES.md` 或 `ODM_REPORT_TRACKING.md`。
5. 若是新系統且有足夠獨立規則，新增對應文件，例如 `OSS_RULES.md`、`ERP_RULES.md`、`OYM_RULES.md` 或 `STUDIO_RULES.md`。
6. 更新 `SYSTEM_MAP.md`，補上來源索引、系統職責、關聯系統、規則落點、跨系統測試切面與分析狀態。
7. 將可測試規則整理成權限、狀態流、API 欄位、報表/匯出、公式、素材/追蹤碼、跨系統一致性等結構。

## 禁止事項
- 不要根據未驗證推測更新知識庫。
- 不要刪除既有業務邏輯；若規格廢棄，使用刪除線標註並註明版本或來源。
- 不要把 `SYSTEM_MAP.md` 當成全文規格庫；它只放索引與跨系統地圖。
- 不要在未經使用者要求前修改 `sync_from_confluence.py` 的 HTML 清理流程。

## 完成時回報
- 列出更新/新增的 `spec_knowledge` 文件。
- 說明新增了哪些系統或主題索引。
- 若有無法分析的圖片、drawio、mmd、csv 或權限限制，明確列為殘餘風險。
"""


def main() -> int:
    args = parse_args()
    created_at = dt.datetime.now().isoformat(timespec="seconds")

    before = snapshot(SOURCE_ROOTS)
    sync_exit_code: int | None = None
    sync_output: list[str] = []

    if args.no_sync:
        print("[sync-knowledge] --no-sync enabled; skipping Confluence sync.")
    else:
        sync_exit_code, sync_output = run_sync_script()

    after = snapshot(SOURCE_ROOTS)
    source_diff = diff_snapshots(before, after)
    changed_sources = source_diff["added"] + source_diff["modified"]

    report = {
        "created_at": created_at,
        "sync_script": SYNC_SCRIPT,
        "sync_executed": not args.no_sync,
        "sync_exit_code": sync_exit_code,
        "sync_output_tail": sync_output[-80:],
        "source_roots": list(SOURCE_ROOTS),
        "source_diff": source_diff,
        "candidate_systems": classify_paths(changed_sources),
        "spec_docs": sorted(rel(path) for path in iter_files([SPEC_ROOT])),
        "git_status": git_status([*SOURCE_ROOTS, SPEC_ROOT]),
    }

    color_enabled = not args.no_color and os.getenv("NO_COLOR") is None and sys.stdout.isatty()
    style = Style(color_enabled)
    print(build_terminal_summary(report, args.max_files, args.view, style))

    if args.write_report:
        run_id = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = ROOT / ".sync_reports"
        report_dir.mkdir(parents=True, exist_ok=True)

        json_path = report_dir / f"sync_knowledge_{run_id}.json"
        markdown_path = report_dir / f"sync_knowledge_{run_id}.md"
        prompt_path = report_dir / f"sync_knowledge_handoff_{run_id}.md"

        write_json(json_path, report)
        prompt = build_handoff_prompt(report, args.max_files)
        prompt_path.write_text(prompt, encoding="utf-8")
        markdown = build_markdown_report(report, args.max_files)
        markdown_path.write_text(markdown, encoding="utf-8")

        print("[sync-knowledge] Report written:")
        print(f"  - {rel(json_path)}")
        print(f"  - {rel(markdown_path)}")
        print(f"  - {rel(prompt_path)}")

    return 0 if sync_exit_code in (None, 0) else sync_exit_code


if __name__ == "__main__":
    raise SystemExit(main())
