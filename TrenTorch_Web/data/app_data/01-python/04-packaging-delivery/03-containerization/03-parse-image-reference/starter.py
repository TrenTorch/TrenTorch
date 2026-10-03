import re

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def parse_image_ref(ref: str) -> dict:
    """
    Parse an image reference like "[registry[:port]/]name[:tag][@digest]".

    Return {"name": ..., "tag": ..., "digest": ..., "pinned": ...}:
      - "digest": the text after "@" (e.g. "sha256:ab12..."), or None
      - "tag": the text after the colon in the LAST "/"-separated
        segment of the name, or None. If there is no tag and no digest,
        the tag is "latest".
      - "name": the reference without its tag and digest (a registry
        host:port keeps its colon)
      - "pinned": True only if the digest is "sha256:" followed by
        exactly 64 lowercase hex characters
    """
    # TODO: implement this, see the Theory tab for the rules.
    pass
