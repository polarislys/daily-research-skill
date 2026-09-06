#!/usr/bin/env python3
"""从收件箱 + 当日 output 文章生成邮件 digest（HTML + 纯文本）。"""

from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPO_ROOT / "output"
INBOX_DIR = OUTPUT / "收件箱"
GITHUB_REPO = "https://github.com/polarislys/daily-research-skill"


def shanghai_today() -> str:
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz).strftime("%Y-%m-%d")


def read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def parse_inbox_stats(body: str) -> dict[str, str]:
    stats: dict[str, str] = {}
    for line in body.splitlines():
        m = re.match(r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if not m:
            continue
        key, val = m.group(1).strip(), m.group(2).strip()
        if key in ("指标", "---") or val == "---":
            continue
        stats[key] = val
    return stats


def parse_deep_links(body: str) -> list[str]:
    section = re.search(r"## 深写链接\s*\n+(```text\n(.*?)\n```)", body, re.S)
    if not section:
        return []
    lines = []
    for line in section.group(2).splitlines():
        line = line.strip()
        if line.startswith("- "):
            lines.append(line[2:])
    return lines


def find_articles_for_date(date: str) -> list[dict[str, str]]:
    articles: list[dict[str, str]] = []
    for md in sorted(OUTPUT.rglob(f"*-{date}.md")):
        if "收件箱" in md.parts:
            continue
        rel = md.relative_to(OUTPUT)
        parts = rel.parts
        track = parts[0] if parts else ""
        theme = parts[1] if len(parts) > 2 else ""
        title = md.stem.replace(f"-{date}", "")
        articles.append(
            {
                "track": track,
                "theme": theme,
                "title": title,
                "path": str(rel).replace("\\", "/"),
                "url": f"{GITHUB_REPO}/blob/main/output/{rel.as_posix()}",
            }
        )
    return articles


def first_heading(md_path: Path) -> str:
    for line in read_text(md_path).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md_path.stem


def build_digest(date: str) -> tuple[str, str, str]:
    inbox_path = INBOX_DIR / f"{date}.md"
    inbox_body = read_text(inbox_path)
    stats = parse_inbox_stats(inbox_body)
    deep_links = parse_deep_links(inbox_body)
    articles = find_articles_for_date(date)

    subject = f"Daily Research {date}"
    if stats.get("实际深写"):
        subject += f" · {stats['实际深写']} 篇深写"

    text_lines = [
        f"Daily Research — {date}",
        f"仓库: {GITHUB_REPO}",
        "",
        "【收件箱统计】",
    ]
    for k, v in stats.items():
        text_lines.append(f"  {k}: {v}")

    if deep_links:
        text_lines.extend(["", "【深写链接】"])
        text_lines.extend(f"  · {x}" for x in deep_links)

    text_lines.extend(["", "【当日文章】"])
    if articles:
        for a in articles:
            text_lines.append(f"  [{a['track']}] {a['theme']} — {a['title']}")
            text_lines.append(f"    {a['url']}")
    else:
        text_lines.append("  （无当日深写文件）")

    if inbox_path.is_file():
        text_lines.extend(["", "【收件箱全文】", f"  {GITHUB_REPO}/blob/main/output/收件箱/{date}.md"])

    text_body = "\n".join(text_lines)

    html_parts = [
        f"<h1>Daily Research — {html.escape(date)}</h1>",
        f'<p><a href="{GITHUB_REPO}">polarislys/daily-research-skill</a></p>',
        "<h2>收件箱统计</h2><ul>",
    ]
    for k, v in stats.items():
        html_parts.append(f"<li><strong>{html.escape(k)}</strong>: {html.escape(v)}</li>")
    html_parts.append("</ul>")

    if articles:
        html_parts.append("<h2>当日文章</h2><ul>")
        for a in articles:
            heading = first_heading(OUTPUT / a["path"])
            html_parts.append(
                f'<li>[{html.escape(a["track"])}] <strong>{html.escape(a["theme"])}</strong> — '
                f'<a href="{a["url"]}">{html.escape(heading)}</a></li>'
            )
        html_parts.append("</ul>")

    if inbox_path.is_file():
        inbox_url = f"{GITHUB_REPO}/blob/main/output/收件箱/{date}.md"
        html_parts.append(f'<p><a href="{inbox_url}">查看完整收件箱</a></p>')

    html_body = "\n".join(html_parts)
    return subject, text_body, html_body


def main() -> int:
    parser = argparse.ArgumentParser(description="Build daily research email digest")
    parser.add_argument("--date", default=shanghai_today(), help="YYYY-MM-DD (default: Asia/Shanghai today)")
    parser.add_argument("--out-dir", type=Path, help="Write digest.txt and digest.html here")
    args = parser.parse_args()

    subject, text_body, html_body = build_digest(args.date)

    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "subject.txt").write_text(subject, encoding="utf-8")
        (args.out_dir / "digest.txt").write_text(text_body, encoding="utf-8")
        (args.out_dir / "digest.html").write_text(html_body, encoding="utf-8")
        print(f"Wrote digest to {args.out_dir}")
    else:
        print("SUBJECT:", subject)
        print("---")
        print(text_body)

    return 0


if __name__ == "__main__":
    sys.exit(main())
