"""Build the profile site from the Markdown files in content/.

Usage:
    python build.py            # writes the site to _site/
    python build.py --serve    # builds, then serves it at http://localhost:8000

You never need to edit this file to change the site's content.
Edit content/profile.md and the files in content/sections/ instead.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import shutil
import sys
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
SECTIONS = CONTENT / "sections"
THEME = ROOT / "theme"
ASSETS = ROOT / "assets"
OUT = ROOT / "_site"

FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.S)
LAYOUTS = {"prose", "entries", "bios", "tags"}


def read_markdown_file(path: Path) -> tuple[dict, str]:
    """Split a Markdown file into (front matter dict, body text)."""
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(text)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    if not isinstance(meta, dict):
        sys.exit(f"{path}: the block between the --- lines must be 'key: value' pairs")
    return meta, match.group(2)


def to_html(text: str) -> str:
    md = markdown.Markdown(extensions=["extra", "attr_list", "sane_lists", "smarty"])
    return md.convert(text)


ENTRY_HEAD = re.compile(r"^\s*(<h3[^>]*>.*?</h3>)\s*(<p class=\"meta\">.*?</p>)?", re.S)


def split_entries(body_html: str) -> tuple[str, list[dict]]:
    """Split rendered HTML at each <h3>.

    Returns (intro, entries), where each entry has a 'head' (the heading and an
    optional `{: .meta }` line under it) and a 'body' (everything else).
    """
    parts = re.split(r"(?=<h3[\s>])", body_html)
    intro = "" if parts[0].lstrip().startswith("<h3") else parts[0]
    entries = []
    for part in parts:
        match = ENTRY_HEAD.match(part)
        if match:
            entries.append({"head": match.group(0).strip(), "body": part[match.end():].strip()})
    return intro, entries


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_sections() -> list[dict]:
    sections = []
    for path in sorted(SECTIONS.glob("*.md")):
        meta, body = read_markdown_file(path)
        if meta.get("hidden"):
            continue
        layout = meta.get("layout", "prose")
        if layout not in LAYOUTS:
            sys.exit(f"{path.name}: layout must be one of {sorted(LAYOUTS)}, got '{layout}'")
        title = meta.get("title") or path.stem.split("-", 1)[-1].replace("-", " ").title()
        body_html = to_html(body)
        intro, entries = split_entries(body_html) if layout != "prose" else (body_html, [])
        sections.append(
            {
                "id": meta.get("id") or slugify(path.stem.split("-", 1)[-1]),
                "title": title,
                "nav": meta.get("nav", title),
                "show_in_nav": meta.get("show_in_nav", True),
                "lead": meta.get("lead", ""),
                "layout": layout,
                "intro": intro,
                "entries": entries,
            }
        )
    return sections


def load_profile() -> dict:
    meta, body = read_markdown_file(CONTENT / "profile.md")
    for key in ("name", "headline"):
        if not meta.get(key):
            sys.exit(f"content/profile.md: '{key}' is required")
    meta["intro_html"] = to_html(body)
    meta.setdefault("initials", "".join(w[0] for w in meta["name"].split()[:2]).upper())
    meta["pipeline"] = meta.get("pipeline") or []
    for key in ("resume", "photo"):
        value = meta.get(key)
        if value and not (ASSETS / Path(value).name).exists():
            print(f"warning: {key} '{value}' not found in assets/, hiding it", file=sys.stderr)
            meta[key] = ""
    return meta


def build() -> None:
    profile = load_profile()
    sections = load_sections()

    env = Environment(
        loader=FileSystemLoader(THEME),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    page = env.get_template("template.html").render(
        profile=profile,
        sections=sections,
        year=dt.date.today().year,
        built=dt.date.today().strftime("%B %Y"),
    )

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "index.html").write_text(page, encoding="utf-8")
    for name in ("style.css", "site.js"):
        shutil.copy(THEME / name, OUT / name)
    if ASSETS.exists():
        shutil.copytree(ASSETS, OUT / "assets")
    (OUT / ".nojekyll").write_text("")
    site_url = profile.get("site_url", "").rstrip("/")
    if site_url:
        (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n")
        (OUT / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"<url><loc>{html.escape(site_url)}/</loc></url></urlset>\n"
        )
    print(f"Built {len(sections)} sections into {OUT.relative_to(ROOT)}/")


def serve(port: int) -> None:
    import functools
    import http.server

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
    print(f"Serving at http://localhost:{port}  (Ctrl+C to stop; re-run to pick up edits)")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--serve", action="store_true", help="serve the built site locally")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    build()
    if args.serve:
        serve(args.port)
