import re

_PINNED = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*(\[[^\]]*\])?\s*==\s*[^\s*,=<>!~]+$")


def find_unpinned(requirements: list[str]) -> list[str]:
    """
    `requirements` is the list of lines of a requirements.txt file.
    Return, in their original order, the requirements that are NOT
    pinned to an exact version.

    Clean each line before judging it:
      - a line that is blank, or starts with `#`, is ignored
      - cut off an inline comment (everything from " #")
      - cut off options (everything from " --", e.g. " --hash=...")
      - remove a trailing backslash continuation
      - remove an environment marker (everything from ";")
      - a cleaned line that is empty or starts with "-" (such as
        "--require-hashes") is ignored

    A cleaned requirement is pinned if it is `name==version` (optionally
    `name[extra]==version`) where the version has no `*` and no `,`, or
    if it is a direct reference containing " @ ".

    Return the cleaned text of each unpinned requirement.
    """
    # TODO: implement this, see the Theory tab for the rules.
    pass
