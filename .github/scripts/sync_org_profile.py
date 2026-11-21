#!/usr/bin/env python3
"""
Builds the README shown on https://github.com/TrenTorch (the org profile) from
this repo's README.md.

GitHub renders the org profile from profile/README.md in the TrenTorch/.github
repo, which is a different repo from this one, so every relative link and
image in README.md (`.github/assets/hero-light.svg`, `LICENSE`,
`TrenTorch_CLI/docs/...`) would break there. This rewrites them to absolute
URLs on TrenTorch-Dev and leaves everything else alone: anchors (`#faq`),
absolute URLs, mailto links, and anything inside a fenced code block.

Images (src / srcset / an image extension) point at raw.githubusercontent.com;
other links point at github.com/.../blob/.

Run by .github/workflows/sync-org-profile.yml:
    python3 .github/scripts/sync_org_profile.py README.md org-profile/profile/README.md
    python3 .github/scripts/sync_org_profile.py --selftest
"""

import re
import sys
from pathlib import Path

REPO = "TrenTorch/TrenTorch"
BRANCH = "TrenTorch-Dev"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/"
BLOB = f"https://github.com/{REPO}/blob/{BRANCH}/"
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")

# `](target)` or `](target "title")`
MD_LINK = re.compile(r'\]\((?P<url>[^)\s]+)(?P<title>\s+"[^"]*")?\)')
# src="x", srcset="x", href="x" (single or double quotes)
HTML_ATTR = re.compile(
    r"""\b(?P<attr>src|srcset|href)=(?P<q>["'])(?P<url>[^"']*)(?P=q)"""
)


def is_relative(url: str) -> bool:
    return bool(url) and not (
        url.startswith(("#", "/"))
        or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url)  # https:, mailto:, data:, ...
    )


def absolute(url: str, *, image: bool) -> str:
    if not is_relative(url):
        return url
    path = url.removeprefix("./")
    base = (
        RAW
        if image or path.split("#")[0].split("?")[0].lower().endswith(IMAGE_EXTENSIONS)
        else BLOB
    )
    return base + path


def rewrite_line(line: str) -> str:
    line = MD_LINK.sub(
        lambda m: f"]({absolute(m['url'], image=False)}{m['title'] or ''})", line
    )
    return HTML_ATTR.sub(
        lambda m: (
            f"{m['attr']}={m['q']}{absolute(m['url'], image=m['attr'] != 'href')}{m['q']}"
        ),
        line,
    )


def convert(markdown: str) -> str:
    out = []
    fence = None  # the opening fence marker while inside a fenced code block
    for line in markdown.split("\n"):
        stripped = line.lstrip()
        marker = stripped[:3] if stripped[:3] in ("```", "~~~") else None
        if fence is None and marker:
            fence = marker
            out.append(line)
        elif fence is not None:
            if marker == fence:
                fence = None
            out.append(line)
        else:
            out.append(rewrite_line(line))
    return "\n".join(out)


def selftest() -> None:
    cases = {
        # markdown links and images
        "[Contributing](CONTRIBUTING.md)": f"[Contributing]({BLOB}CONTRIBUTING.md)",
        "[Doc](TrenTorch_CLI/docs/a.md#top)": f"[Doc]({BLOB}TrenTorch_CLI/docs/a.md#top)",
        "[License](LICENSE)": f"[License]({BLOB}LICENSE)",
        "![x](.github/assets/a.png)": f"![x]({RAW}.github/assets/a.png)",
        # a badge: image inside a link, only the relative parts change
        "[![License](https://img.shields.io/b.svg)](LICENSE)": (
            f"[![License](https://img.shields.io/b.svg)]({BLOB}LICENSE)"
        ),
        '[a](docs/x.md "Title")': f'[a]({BLOB}docs/x.md "Title")',
        "[a](./docs/x.md)": f"[a]({BLOB}docs/x.md)",
        # html
        '<img src=".github/assets/a.svg" width="100%" />': (
            f'<img src="{RAW}.github/assets/a.svg" width="100%" />'
        ),
        '<source media="(prefers-color-scheme: dark)" srcset=".github/assets/d.svg" />': (
            f'<source media="(prefers-color-scheme: dark)" srcset="{RAW}.github/assets/d.svg" />'
        ),
        '<a href="TrenTorch_Web/README.md">web</a>': f'<a href="{BLOB}TrenTorch_Web/README.md">web</a>',
        # left alone
        "[Quickstart](#quickstart)": "[Quickstart](#quickstart)",
        "[Site](https://trentorch.com)": "[Site](https://trentorch.com)",
        "[Mail](mailto:a@b.co)": "[Mail](mailto:a@b.co)",
        '<a href="https://x.dev">x</a>': '<a href="https://x.dev">x</a>',
        "[Root](/docs)": "[Root](/docs)",
    }
    for source, expected in cases.items():
        got = convert(source)
        assert got == expected, (
            f"{source!r}\n  got      {got!r}\n  expected {expected!r}"
        )

    fenced = '```bash\n[a](b.md)\n<img src="x.png">\n```\n[a](b.md)'
    assert (
        convert(fenced)
        == f'```bash\n[a](b.md)\n<img src="x.png">\n```\n[a]({BLOB}b.md)'
    ), "fences"
    tilde = "~~~\n[a](b.md)\n~~~"
    assert convert(tilde) == tilde, "tilde fence"
    # a longer sample: nothing relative may survive outside code fences
    sample = '<picture><source srcset=".github/assets/h.svg"/><img src=".github/assets/h.svg"/></picture>\n[A](a.md) [B](#b)'
    result = convert(sample)
    assert 'src=".github' not in result and "](a.md)" not in result, result
    assert convert(convert(sample)) == result, "must be idempotent"
    print(f"selftest ok ({len(cases) + 4} checks)")


def main(argv: list[str]) -> int:
    if argv == ["--selftest"]:
        selftest()
        return 0
    if len(argv) != 2:
        print(__doc__)
        return 2
    source, target = Path(argv[0]), Path(argv[1])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(convert(source.read_text(encoding="utf-8")), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
