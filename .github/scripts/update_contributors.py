#!/usr/bin/env python3
"""
Regenerates the "Team Engineers" and "Open-Source Contributors" avatar grids
directly inside README.md from real GitHub data. Only people with at least
one merged PR get a spot (a closed-without-merging PR earns no credit, and
raising an issue alone does not earn a spot; issues are still counted next
to the name). Renders an avatar grid
(the good part of the all-contributors project's UI) with plain-text stats
instead of an emoji contribution-type key (the part we're deliberately not
copying). Preserves each person's existing hand-written intro line; a
first-time contributor gets a generic placeholder intro instead of a
fabricated bio, since nobody should get credentials invented for them.

This used to write a separate docs/CONTRIBUTORS.md, with a hand-maintained
"Team Engineers" table duplicated (and already drifted -- missing a real
contributor, no PR/issue counts) directly in README.md alongside it. Two
places to keep in sync is how it drifted in the first place -- now there's
one real table, generated, living where people actually look for it.

Run by .github/workflows/update-contributors.yml, authenticated with
GITHUB_TOKEN via the gh CLI (already configured by actions/checkout /
the workflow's GH_TOKEN env var).
"""

import base64
import json
import math
import re
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO = "TrenTorch/TrenTorch"
ROOT = Path(__file__).resolve().parent.parent.parent
README_FILE = ROOT / "README.md"
DEFAULT_INTRO = "Spots bugs, fixes them & contributes"
# Placeholder intros written by earlier versions of this script. They are
# upgraded to DEFAULT_INTRO so the whole grid reads the same.
LEGACY_DEFAULT_INTROS = {"Spots bugs, corrects them and contributes"}

# Intro convention: one or two short lines, joined with <br />, no full
# stops, "&" instead of "and". Line one is where someone studies or works,
# line two is the tagline, e.g. "IIT Guwahati<br />Catches bugs & ships fast".
LINE_BREAK = "<br />"
COLUMNS = 4

# The README's problem count follows what trentorch.com shows. The status
# page's Worker reads it off the home page and republishes it as JSON. We
# ask its workers.dev address because trentorch.com's bot protection can
# challenge GitHub's runners. SITE_STATS_URL overrides it for testing.
SITE_STATS_URL = os.environ.get(
    "SITE_STATS_URL", "https://trentorch-status.shashanktripathi07.workers.dev/api/site-stats"
)
QUESTION_COUNT_RE = re.compile(r"(<!-- question-count -->)[^<]*(<!-- /question-count -->)")

# The two code owners always lead the Team Engineers table, in this order.
# Everyone else, in both grids, is ordered by activity (merged PRs plus
# issues, most first), so nobody has to be hand-placed.
FIXED_TEAM_HEAD = ["Shashank-Tripathi-07", "ShivtejG236"]

# Custom avatar images checked into the repo, used instead of the person's
# live GitHub avatar URL. Add an entry here (and the image under
# .github/assets/) for anyone who wants their own picture instead of
# whatever's on their GitHub profile. Path is relative to README.md (the
# repo root), since that's the only file this grid renders in now.
AVATAR_OVERRIDES = {
    "Shashank-Tripathi-07": ".github/assets/rocky-avatar.png",
}

# Role tag shown right under each person's name. PROJECT_LEAD_LOGIN /
# CORE_ENGINEERS mirror maintainer-badge.yml's own hardcoded roster by hand
# (keep both in sync); everyone else gets "Maintainer" if they hold live
# Maintain/Admin repo permission, computed fresh each run same as
# maintainer-badge.yml does, or no role line at all for outside
# contributors.
PROJECT_LEAD_LOGIN = "Shashank-Tripathi-07"
CORE_ENGINEERS = {"yashanand12ssdn-ops"}

# What the Team Engineers table shows under each name. The role above
# (resolve_role) still decides who counts as team; this is only the label.
ROLE_TITLES = {
    "Shashank-Tripathi-07": "Principal Maintainer & Infrastructure Architect",
    "ShivtejG236": "Maintainer & Head of EngOps",
    "maanas1234": "Maintainer & Core Engineer",
    "aadityansha06": "Maintainer & Growth Lead",
}

# Avatars are rendered as squircles. GitHub strips CSS from a README, so
# the rounding is baked into a small SVG per person, kept under this folder
# (relative to the repo root) with the photo embedded in it.
AVATAR_DIR = ".github/assets/avatars"
AVATAR_PX = 192  # source size embedded in each SVG; shown smaller in the README
SHOWN_PX = 96


def resolve_role(login: str) -> str | None:
    if login == PROJECT_LEAD_LOGIN:
        return "Principal Maintainer"
    if login in CORE_ENGINEERS:
        return "Core Engineer"
    try:
        perm = subprocess.run(
            ["gh", "api", f"repos/{REPO}/collaborators/{login}/permission", "--jq", ".role_name"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        return None  # not a collaborator (e.g. left the org) -- no role line
    return "Maintainer" if perm in ("maintain", "admin") else None


# The repo was private when this script was first written, so shields.io
# couldn't query the real GitHub API for a live contributor count -- this
# badge is a static image whose count this script keeps in sync manually
# instead. Now public (moved to the TrenTorch org), but left as a static
# badge rather than switching to a live query, since that's an unrelated
# behavior change from what this script is here to do. Links to the
# in-README section now, not a separate file.
BADGE_RE = re.compile(
    r"\[!\[Contributors\]\(https://img\.shields\.io/badge/contributors-\d+-orange\.svg\)\]\([^)]*\)"
)

CELL_RE = re.compile(
    r'<a href="https://github\.com/([^"]+)">'
    r'<img[^>]*alt="([^"]*)"\s*/?>'
    r"</a>\s*<br\s*/?>\s*"
    r"<b>([^<]+)</b>\s*<br\s*/?>\s*"
    # The role line (added after this regex was first written) sits between
    # the name and the intro now -- <sub><strong>Role</strong></sub>, which
    # a plain <sub>([^<]*)</sub> can't match through, since <strong> is a
    # "<" this character class rejects. Skip it first, optionally, so a
    # contributor without a role line (external, no live permission) still
    # matches too. This exact bug wiped every real name/bio back to raw
    # logins on this regex's first run after the role line was added --
    # confirmed live, not assumed.
    r"(?:<sub><strong>[^<]*</strong></sub>\s*<br\s*/?>\s*)?"
    r"<sub>((?:[^<]|<br\s*/?>)*)</sub>",
    re.DOTALL,
)

# The README has two generated sections, one per group: the maintainers
# ("## Team Engineers") and everyone else ("## Open-Source Contributors").
# Each regex replaces what sits between its own heading and the next
# "---" divider (README's own section-separator convention). The team
# section ends at the contributors heading, and the contributors section
# ends at the divider after it.
TEAM_SECTION_RE = re.compile(
    r"(## Team Engineers\n\n).*?(\n\n---\n\n## Open-Source Contributors)",
    re.DOTALL,
)
CONTRIBUTORS_SECTION_RE = re.compile(
    r"(## Open-Source Contributors\n\n).*?(\n\n---)",
    re.DOTALL,
)

# Roles that put someone in the Team Engineers section. Everyone else,
# including people with no role line, goes under Open-Source Contributors.
TEAM_ROLES = {"Principal Maintainer", "Maintainer", "Core Engineer"}


def gh_json(args):
    result = subprocess.run(
        ["gh"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True
    )
    return json.loads(result.stdout)


# A person credited as `Co-authored-by:` on a commit in a merged PR earns a
# spot the same way the PR's own author does -- someone who found a bug or
# wrote the fix that got folded into someone else's PR shouldn't need a
# separate PR of their own just to show up here. Only the standard
# GitHub-generated noreply address (`id+login@users.noreply.github.com`) is
# resolved, since that's the only form that maps back to a login without an
# extra API call per email address.
CO_AUTHOR_RE = re.compile(
    r"^Co-authored-by:\s*.*?<\d+\+([^@]+)@users\.noreply\.github\.com>",
    re.MULTILINE,
)


def fetch_co_author_logins(pr_number: int) -> set[str]:
    commits = gh_json(["pr", "view", str(pr_number), "--repo", REPO, "--json", "commits"])
    logins = set()
    for commit in commits.get("commits", []):
        body = commit.get("messageBody", "") or ""
        logins.update(CO_AUTHOR_RE.findall(body))
    return logins


# A PR earns its author contributor credit only once it's actually been
# accepted. `gh pr list --state all` returns OPEN, MERGED, and CLOSED
# (closed WITHOUT merging -- i.e. rejected) alike; treating "any state" or
# even "not open" as "counts" silently credits a PR a maintainer rejected
# the exact same as one they merged. This is a pure, unit-tested function
# (see selftest_pr_filtering below) specifically so that regression can't
# creep back in unnoticed the way it did once already -- any future edit
# to this logic gets checked by --selftest, run by the workflow before it
# ever touches README.md for real.
def counts_toward_contribution(pr: dict) -> bool:
    return not pr["author"].get("is_bot") and pr.get("state") == "MERGED"


def fetch_counts():
    prs = gh_json(
        ["pr", "list", "--repo", REPO, "--state", "all", "--limit", "1000", "--json", "number,author,state"]
    )
    issues = gh_json(
        ["issue", "list", "--repo", REPO, "--state", "all", "--limit", "1000", "--json", "author"]
    )

    counts = {}

    def bucket(login):
        return counts.setdefault(login, {"issues": 0, "prs": 0})

    for pr in prs:
        if not counts_toward_contribution(pr):
            continue
        login = pr["author"]["login"]
        bucket(login)["prs"] += 1
        for co_login in fetch_co_author_logins(pr["number"]):
            if co_login != login and not is_bot_login(co_login):
                bucket(co_login)["prs"] += 1

    for issue in issues:
        if issue["author"].get("is_bot"):
            continue
        login = issue["author"]["login"]
        bucket(login)["issues"] += 1

    return only_pr_authors(counts)


def only_pr_authors(counts: dict) -> dict:
    """Keeps only people with at least one merged PR. Raising an issue
    still shows up in the Issues count next to a name, but on its own it
    does not earn a spot in either grid. Pure, so --selftest can check it."""
    return {login: c for login, c in counts.items() if c["prs"] > 0}


def normalize_intro(intro: str) -> str:
    """Brings an intro in line with the convention: no trailing full stop,
    one tidy <br /> between lines, and the legacy placeholder upgraded."""
    intro = re.sub(r"\s*<br\s*/?>\s*", LINE_BREAK, intro.strip())
    intro = intro.rstrip(". ").strip()
    intro = re.sub(r"&(?!#?\w+;)", "&amp;", intro)  # a bare & is escaped for valid HTML
    return DEFAULT_INTRO if intro in LEGACY_DEFAULT_INTROS else intro


def parse_existing(content: str):
    """Returns {login: (name, intro)} scraped from the current avatar grid,
    so a re-run doesn't clobber hand-written names/intros with placeholders."""
    existing = {}
    for login, _alt, name, intro in CELL_RE.findall(content):
        existing[login] = (name.strip(), normalize_intro(intro))
    return existing


def squircle_path(size: int, n: float = 5.0, steps: int = 120) -> str:
    """An SVG path for a squircle (superellipse) filling a size x size box.
    n=2 is a circle, large n approaches a square; 5 gives the soft iOS-style
    corner."""
    half = size / 2
    points = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        cos, sin = math.cos(t), math.sin(t)
        x = half + half * math.copysign(abs(cos) ** (2 / n), cos)
        y = half + half * math.copysign(abs(sin) ** (2 / n), sin)
        points.append(f"{x:.2f},{y:.2f}")
    return "M" + " L".join(points) + " Z"


def squircle_svg(image: bytes, mime: str, size: int = AVATAR_PX) -> str:
    """A self-contained SVG: the photo clipped to a squircle with a faint
    outline that reads on both light and dark GitHub themes."""
    path = squircle_path(size)
    data = base64.b64encode(image).decode("ascii")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        f'<defs><clipPath id="s"><path d="{path}"/></clipPath></defs>'
        f'<image width="{size}" height="{size}" preserveAspectRatio="xMidYMid slice" clip-path="url(#s)" '
        f'xlink:href="data:{mime};base64,{data}"/>'
        f'<path d="{path}" fill="none" stroke="#8b949e" stroke-opacity="0.45" stroke-width="2"/>'
        f"</svg>\n"
    )


def download_avatar(login: str):
    """(bytes, mime) for the login's GitHub photo, or None on failure."""
    url = f"https://avatars.githubusercontent.com/{login}?s={AVATAR_PX}&v=4"
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "TrenTorch-README-Updater"})
        with urllib.request.urlopen(request, timeout=20) as response:
            mime = response.headers.get_content_type()
            body = response.read()
    except OSError as err:
        print(f"warning: could not fetch the avatar for {login} ({err})", file=sys.stderr)
        return None
    return (body, mime) if mime.startswith("image/") and body else None


def avatar_src(login: str) -> str:
    """Writes the login's squircle SVG under AVATAR_DIR and returns its
    path for the README. If the photo can't be fetched, keeps the SVG from
    the last run, or else falls back to the plain GitHub URL."""
    safe = re.sub(r"[^A-Za-z0-9-]", "", login) or "unknown"
    relative = f"{AVATAR_DIR}/{safe}.svg"
    target = ROOT / relative
    override = AVATAR_OVERRIDES.get(login)
    if override:
        source = ROOT / override
        image = (source.read_bytes(), "image/png" if source.suffix == ".png" else "image/jpeg")
    else:
        image = download_avatar(login)
    if image is None:
        return relative if target.exists() else f"https://avatars.githubusercontent.com/{login}?v=4"
    svg = squircle_svg(*image)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or target.read_text(encoding="utf-8") != svg:
        target.write_text(svg, encoding="utf-8")
    return relative


def is_bot_login(login: str) -> bool:
    """Bots never earn a spot. GitHub marks real bot accounts with a
    "[bot]" suffix, and Copilot's co-author trailer names it plainly."""
    return login.lower().endswith("[bot]") or login.lower() == "copilot"


def activity_key(login: str, counts: dict):
    """Most active first: merged PRs plus issues, then PRs, then name."""
    c = counts.get(login, {"prs": 0, "issues": 0})
    return (-(c["prs"] + c["issues"]), -c["prs"], login.lower())


def split_by_role(logins, roles: dict, counts: dict):
    """Splits logins into (team, contributors) by role. The code owners in
    FIXED_TEAM_HEAD lead the team list in that order, then the rest of the
    team by activity. Contributors are ordered by activity too. Pure, so
    --selftest can check it without the network."""

    def team_sort_key(login: str):
        if login in FIXED_TEAM_HEAD:
            return (0, FIXED_TEAM_HEAD.index(login), ())
        return (1, 0, activity_key(login, counts))

    team = sorted((login for login in logins if roles.get(login) in TEAM_ROLES), key=team_sort_key)
    contributors = sorted(
        (login for login in logins if roles.get(login) not in TEAM_ROLES),
        key=lambda login: activity_key(login, counts),
    )
    return team, contributors


def parse_site_stats(body: str):
    """The problem count from the status Worker's JSON, or None if the body
    isn't what we expect. Pure, so --selftest can check it."""
    try:
        problems = json.loads(body).get("problems")
    except (ValueError, AttributeError):
        return None
    if isinstance(problems, int) and not isinstance(problems, bool) and 0 < problems <= 1_000_000:
        return problems
    return None


def fetch_question_count():
    """The live problem count, or None when it can't be read (the README
    then keeps its current number)."""
    try:
        request = urllib.request.Request(SITE_STATS_URL, headers={"User-Agent": "TrenTorch-README-Updater"})
        with urllib.request.urlopen(request, timeout=20) as response:
            count = parse_site_stats(response.read().decode("utf-8", "replace"))
    except OSError as err:
        print(f"warning: could not fetch the problem count ({err}); leaving it unchanged", file=sys.stderr)
        return None
    if count is None:
        print("warning: unexpected response for the problem count; leaving it unchanged", file=sys.stderr)
    return count


def update_question_count(content: str, count: int):
    """Writes count between every pair of question-count markers. Returns
    (new_content, markers_found)."""
    return QUESTION_COUNT_RE.subn(lambda m: f"{m.group(1)}{count}{m.group(2)}", content)


def build_table(logins, counts: dict, existing: dict, roles: dict) -> str:
    cells = []
    width = round(100 / COLUMNS, 2)
    for login in logins:
        c = counts[login]
        name, intro = existing.get(login, (login, DEFAULT_INTRO))
        photo = avatar_src(login)
        stats = f"Issues: {c['issues']} &middot; PRs: {c['prs']}"
        role = ROLE_TITLES.get(login, roles.get(login))
        role = role.replace("&", "&amp;") if role else role
        role_html = f"        <sub><strong>{role}</strong></sub>\n        <br />\n" if role else ""
        cells.append(
            f'      <td align="center" valign="top" width="{width}%">\n'
            f'        <a href="https://github.com/{login}">'
            f'<img src="{photo}" width="{SHOWN_PX}" height="{SHOWN_PX}" alt="{name}"/></a>\n'
            f"        <br />\n"
            f"        <b>{name}</b>\n"
            f"        <br />\n"
            f"{role_html}"
            f"        <sub>{intro}</sub>\n"
            f"        <br />\n"
            f"        <sub>{stats}</sub>\n"
            f"      </td>"
        )

    rows = []
    for i in range(0, len(cells), COLUMNS):
        row_cells = "\n".join(cells[i : i + COLUMNS])
        rows.append(f"    <tr>\n{row_cells}\n    </tr>")

    return '<table width="100%" style="width:100%">\n  <tbody>\n' + "\n".join(rows) + "\n  </tbody>\n</table>"


TEAM_INTRO = (
    "The maintainers, code owners first and then most active first (PRs plus issues). Counts are recomputed whenever a PR merges, from real issue/PR activity via "
    "[`.github/workflows/update-contributors.yml`](.github/workflows/update-contributors.yml).\n\n"
)

CONTRIBUTORS_INTRO = (
    "Everyone else who has had a PR merged, most active first (PRs plus issues), or is credited as a `Co-authored-by:` on one. Want to show "
    "up here? Get a PR merged, or get credited as a co-author on someone else's: the first-contribution "
    "bot will say hello on your first PR, and this grid updates automatically after it merges. A "
    "closed-without-merging PR doesn't count, and neither does an issue on its own.\n\n"
)


def build_grids(counts: dict, existing: dict, roles: dict):
    """Returns (team_block, contributors_block), each intro plus table."""
    team, contributors = split_by_role(list(counts), roles, counts)
    team_block = TEAM_INTRO + build_table(team, counts, existing, roles)
    # Collapsed, since this grid keeps growing and would otherwise push the
    # rest of the README far down the page.
    contributors_block = (
        CONTRIBUTORS_INTRO
        + f"<details>\n<summary>Show all {len(contributors)} contributors</summary>\n\n"
        + build_table(contributors, counts, existing, roles)
        + "\n\n</details>"
    )
    return team_block, contributors_block


def selftest_parser() -> bool:
    """Regression check for the bug that shipped once already: CELL_RE
    failing to match a cell that has a role line, silently wiping the
    person's real name/bio back to their raw login on the next run."""
    sample = (
        '<a href="https://github.com/octocat"><img src="x.png" alt="Octo Cat"/></a>\n'
        "<br />\n"
        "<b>Octo Cat</b>\n"
        "<br />\n"
        "<sub><strong>Maintainer</strong></sub>\n"
        "<br />\n"
        "<sub>IIT Guwahati<br />Builds things &amp; ships.</sub>\n"
        "<br />\n"
        "<sub>Issues: 1 &middot; PRs: 2</sub>"
    )
    found = parse_existing(sample)
    ok = found.get("octocat") == ("Octo Cat", "IIT Guwahati<br />Builds things &amp; ships")
    legacy = normalize_intro("Spots bugs, corrects them and contributes") == DEFAULT_INTRO
    svg = squircle_svg(b"x", "image/png")
    ok = ok and legacy and "<clipPath" in svg and "data:image/png;base64,eA==" in svg
    if not ok:
        print(
            f"selftest_parser FAILED: parse_existing found {found!r}, expected the real name/bio preserved",
            file=sys.stderr,
        )
    return ok


def selftest_pr_filtering() -> bool:
    """Regression check for the bug that shipped once already: a PR
    closed WITHOUT merging (rejected) still counted toward its author's
    contributor credit, because nothing checked PR state at all. Only a
    merged, non-bot PR should count."""
    merged = {"author": {"login": "merged-author", "is_bot": False}, "state": "MERGED"}
    rejected = {"author": {"login": "rejected-author", "is_bot": False}, "state": "CLOSED"}
    still_open = {"author": {"login": "open-author", "is_bot": False}, "state": "OPEN"}
    bot_merged = {"author": {"login": "bot-author", "is_bot": True}, "state": "MERGED"}

    cases = [
        ("a merged PR", merged, True),
        ("a closed-without-merging (rejected) PR", rejected, False),
        ("a still-open PR", still_open, False),
        ("a bot's merged PR", bot_merged, False),
    ]
    ok = True
    for label, pr, expected in cases:
        actual = counts_toward_contribution(pr)
        if actual != expected:
            ok = False
            print(
                f"selftest_pr_filtering FAILED: {label} -> counts_toward_contribution "
                f"returned {actual}, expected {expected}",
                file=sys.stderr,
            )
    return ok


def selftest_co_author_regex() -> bool:
    """A `Co-authored-by:` trailer with the standard GitHub noreply address
    resolves to the login embedded in it; any other address form (can't be
    mapped to a login without a network call) is ignored rather than
    guessed at."""
    body = (
        "Fixes the thing.\n\n"
        "Co-authored-by: Shreya <293188706+Shreyacodess20@users.noreply.github.com>\n"
        "Co-authored-by: Someone Else <someone@example.com>\n"
    )
    found = set(CO_AUTHOR_RE.findall(body))
    ok = found == {"Shreyacodess20"}
    if not ok:
        print(f"selftest_co_author_regex FAILED: got {found!r}, expected {{'Shreyacodess20'}}", file=sys.stderr)
    return ok


def selftest_only_pr_authors() -> bool:
    """Someone who only raised issues gets no grid spot. Someone with a
    merged PR keeps theirs, and their issue count is kept."""
    counts = {
        "issue-only": {"issues": 5, "prs": 0},
        "pr-author": {"issues": 2, "prs": 1},
    }
    result = only_pr_authors(counts)
    ok = result == {"pr-author": {"issues": 2, "prs": 1}}
    if not ok:
        print(f"selftest_only_pr_authors FAILED: got {result!r}", file=sys.stderr)
    return ok


def selftest_split() -> bool:
    """The code owners lead the Team Engineers section (Principal
    Maintainer, then ShivtejG236), the rest of the team and all the
    contributors go by activity (PRs plus issues), and bots are ignored."""
    roles = {
        "aadityansha06": "Maintainer",
        "ShivtejG236": "Maintainer",
        "maanas1234": "Maintainer",
        "Shashank-Tripathi-07": "Principal Maintainer",
        "JashT14": None,
        "outsider": None,
        "newcomer": None,
    }
    counts = {
        "aadityansha06": {"prs": 5, "issues": 1},
        "ShivtejG236": {"prs": 1, "issues": 0},
        "maanas1234": {"prs": 5, "issues": 3},
        "Shashank-Tripathi-07": {"prs": 2, "issues": 0},
        "JashT14": {"prs": 2, "issues": 2},
        "outsider": {"prs": 1, "issues": 0},
        "newcomer": {"prs": 3, "issues": 0},
    }
    logins = ["outsider", "aadityansha06", "ShivtejG236", "newcomer", "maanas1234", "Shashank-Tripathi-07", "JashT14"]
    team, contributors = split_by_role(logins, roles, counts)
    expected_team = ["Shashank-Tripathi-07", "ShivtejG236", "maanas1234", "aadityansha06"]
    expected_contributors = ["JashT14", "newcomer", "outsider"]
    bots_ok = is_bot_login("dependabot[bot]") and is_bot_login("Copilot") and not is_bot_login("JashT14")
    ok = team == expected_team and contributors == expected_contributors and bots_ok
    if not ok:
        print(
            f"selftest_split FAILED: got team={team!r} contributors={contributors!r}, "
            f"expected team={expected_team!r} contributors={expected_contributors!r}, bots_ok={bots_ok}",
            file=sys.stderr,
        )
    return ok


def selftest_question_count() -> bool:
    cell = "| **What** | <!-- question-count -->350+<!-- /question-count --> coding problems |"
    updated, n = update_question_count(cell, 1647)
    ok = (
        parse_site_stats('{"problems":1647,"readAt":1}') == 1647
        and parse_site_stats('{"error":"x"}') is None
        and parse_site_stats("not json") is None
        and parse_site_stats('{"problems":0}') is None
        and parse_site_stats('{"problems":true}') is None
        and n == 1
        and "<!-- question-count -->1647<!-- /question-count -->" in updated
        and update_question_count("no markers", 5)[1] == 0
    )
    if not ok:
        print("selftest_question_count FAILED", file=sys.stderr)
    return ok


def selftest() -> bool:
    """Run via --selftest, and as a pre-flight step in
    update-contributors.yml before this script touches README.md for
    real -- both checks guard against a bug that has already shipped
    once, silently, and only got caught by a human noticing bad output
    in README.md after the fact."""
    results = [
        selftest_parser(),
        selftest_pr_filtering(),
        selftest_co_author_regex(),
        selftest_only_pr_authors(),
        selftest_split(),
        selftest_question_count(),
    ]
    ok = all(results)
    print("selftest passed" if ok else "selftest FAILED", file=sys.stderr if not ok else sys.stdout)
    return ok


def main():
    if "--selftest" in sys.argv:
        return 0 if selftest() else 1

    if not README_FILE.exists():
        print("README.md not found", file=sys.stderr)
        return 1

    content = README_FILE.read_text(encoding="utf-8")
    counts = fetch_counts()
    existing = parse_existing(content)
    roles = {login: resolve_role(login) for login in counts}
    team_block, contributors_block = build_grids(counts, existing, roles)

    new_content, n = TEAM_SECTION_RE.subn(lambda m: m.group(1) + team_block + m.group(2), content, count=1)
    if n == 0:
        print(
            "Could not find the '## Team Engineers' section followed by '## Open-Source Contributors' in README.md",
            file=sys.stderr,
        )
        return 1
    new_content, n = CONTRIBUTORS_SECTION_RE.subn(
        lambda m: m.group(1) + contributors_block + m.group(2), new_content, count=1
    )
    if n == 0:
        print("Could not find the '## Open-Source Contributors' section in README.md", file=sys.stderr)
        return 1

    new_badge = (
        f"[![Contributors](https://img.shields.io/badge/contributors-{len(counts)}-orange.svg)]"
        f"(#team-engineers)"
    )
    new_content, _ = BADGE_RE.subn(new_badge, new_content)

    count = fetch_question_count()
    if count is not None:
        new_content, found = update_question_count(new_content, count)
        if not found:
            print("Could not find the question-count markers in README.md", file=sys.stderr)
            return 1

    if new_content.strip() != content.strip():
        README_FILE.write_text(new_content, encoding="utf-8")
        print("README.md updated")
    else:
        print("No changes")

    return 0


if __name__ == "__main__":
    sys.exit(main())
