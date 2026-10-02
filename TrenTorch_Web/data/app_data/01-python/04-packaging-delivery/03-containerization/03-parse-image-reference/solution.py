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
    name, _, digest_text = ref.partition("@")
    digest = digest_text or None
    prefix, slash, last = name.rpartition("/")
    tag = None
    if ":" in last:
        last, tag = last.rsplit(":", 1)
    name = prefix + slash + last
    if tag is None and digest is None:
        tag = "latest"
    pinned = digest is not None and bool(_DIGEST.match(digest))
    return {"name": name, "tag": tag, "digest": digest, "pinned": pinned}
