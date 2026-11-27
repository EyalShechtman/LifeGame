#!/usr/bin/env python3
"""Split the monolithic index.html into public/index.html + public/src/*.

Mechanical only: no logic changes, no renames. Re-run it whenever a monolithic
index.html (e.g. from an older branch) needs to be brought into the split layout:

    python3 tools/split_index.py [path/to/monolithic/index.html]

Default input is ./index.html at the repo root. Output (overwritten):
    public/index.html        HTML + importmap, links the CSS and loads src/main.js
    public/src/styles.css    the inline <style> block
    public/src/main.js       the inline <script type="module"> minus the pieces below
    public/src/content.js    PLAYERS, DEALER_LOOK, DOG_LOOK, CHAPTERS (pure data)
    public/src/chess-engine.js  Chess (pure rules engine, no DOM/three.js)

Asset paths are rewritten from the repo root to public/assets/ (see ASSETS).
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"

# Top-level declarations moved into their own module, in source order.
# Each must be self-contained (reference nothing else from main.js).
MODULES: dict[str, list[str]] = {
    "content.js": ["PLAYERS", "DEALER_LOOK", "DOG_LOOK", "CHAPTERS"],
    "chess-engine.js": ["Chess"],
}

# Files the site serves, now under public/assets/. A quoted string starting
# with one of these gets "assets/" prepended.
ASSETS = [
    "soccer/", "chess/", "essays/", "dog.webp",
    "dog_head.glb.b64.txt", "dog_rigged.glb.b64.txt", "autumn-leaves.mp3",
]
ASSET_RE = re.compile(r"""(?<=["'`])(%s)""" % "|".join(re.escape(a) for a in ASSETS))


def die(msg: str) -> None:
    sys.exit(f"split_index: {msg}")


def one(pattern: str, lines: list[str], what: str) -> int:
    hits = [i for i, l in enumerate(lines) if re.match(pattern, l)]
    if len(hits) != 1:
        die(f"expected exactly one {what}, found {len(hits)}")
    return hits[0]


def statement_end(lines: list[str], start: int) -> int:
    """Index of the last line of the top-level statement starting at `start`.

    The code puts every top-level statement at column 0 and indents its body,
    so the statement runs until the next column-0 line that isn't a closer."""
    if lines[start].rstrip().endswith(";"):
        return start
    for j in range(start + 1, len(lines)):
        l = lines[j]
        if l and not l[0].isspace():
            if l[0] in "}])":
                if l.rstrip().endswith(";"):
                    return j
                continue
            die(f"statement at script line {start + 1} has no closing line before line {j + 1}")
    die(f"statement at script line {start + 1} never ends")
    return -1


def extract(js: list[str], name: str) -> tuple[list[str], list[str]]:
    i = one(rf"(const|let|var|function|class) {re.escape(name)}\b", js, f"top-level `{name}`")
    j = statement_end(js, i)
    block = js[i:j + 1]
    block[0] = "export " + block[0]
    return js[:i] + js[j + 1:], block


def main() -> None:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "index.html")
    if not src.exists():
        die(f"{src} not found")
    lines = src.read_text(encoding="utf-8").split("\n")

    s0 = one(r"\s*<style>\s*$", lines, "<style>")
    s1 = one(r"\s*</style>\s*$", lines, "</style>")
    m0 = one(r'\s*<script type="module">\s*$', lines, '<script type="module">')
    m1 = next((i for i in range(m0 + 1, len(lines)) if lines[i].strip() == "</script>"), None)
    if m1 is None or not s0 < s1 < m0:
        die("unexpected layout (want <style> ... </style> ... <script type=module> ... </script>)")

    css = lines[s0 + 1:s1]
    js = lines[m0 + 1:m1]
    html = (lines[:s0] + ['<link rel="stylesheet" href="src/styles.css">'] + lines[s1 + 1:m0]
            + ['<script type="module" src="src/main.js"></script>'] + lines[m1 + 1:])

    modules: dict[str, list[str]] = {}
    for fname, names in MODULES.items():
        out: list[str] = []
        for n in names:
            js, block = extract(js, n)
            out += block
        modules[fname] = out

    # import the extracted names right after the last import line of main.js
    last_import = max(i for i, l in enumerate(js) if l.startswith("import "))
    js[last_import + 1:last_import + 1] = [
        f"import {{ {', '.join(names)} }} from './{fname}';" for fname, names in MODULES.items()
    ]

    rewrite = lambda text: ASSET_RE.sub(r"assets/\1", text)
    (OUT / "src").mkdir(parents=True, exist_ok=True)
    files = {
        OUT / "index.html": "\n".join(html),
        OUT / "src" / "styles.css": "\n".join(css) + "\n",
        OUT / "src" / "main.js": "\n".join(js) + "\n",
        **{OUT / "src" / f: "\n".join(b) + "\n" for f, b in modules.items()},
    }
    for path, text in files.items():
        path.write_text(rewrite(text), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)} ({text.count(chr(10))} lines)")

    if shutil.which("node"):
        for path in files:
            if path.suffix == ".js":
                r = subprocess.run(["node", "--check", "--input-type=module"],
                                   input=path.read_text(encoding="utf-8"), text=True, capture_output=True)
                if r.returncode:
                    die(f"{path.name} does not parse:\n{r.stderr}")
        print("node --check: all modules parse")


if __name__ == "__main__":
    main()
