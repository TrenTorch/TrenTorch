"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
parse_image_ref = _module.parse_image_ref


DIGEST = "sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c"


def test_bare_name_defaults_to_latest():
    assert parse_image_ref("python") == {"name": "python", "tag": "latest", "digest": None, "pinned": False}


def test_tag_only_is_not_pinned():
    assert parse_image_ref("python:3.12") == {"name": "python", "tag": "3.12", "digest": None, "pinned": False}


def test_tag_and_digest():
    result = parse_image_ref(f"alpine:3.21@{DIGEST}")
    assert result == {"name": "alpine", "tag": "3.21", "digest": DIGEST, "pinned": True}


def test_digest_only_has_no_default_tag():
    result = parse_image_ref(f"alpine@{DIGEST}")
    assert result["tag"] is None
    assert result["pinned"] is True


def test_registry_port_is_not_a_tag():
    result = parse_image_ref("localhost:5000/team/app")
    assert result == {"name": "localhost:5000/team/app", "tag": "latest", "digest": None, "pinned": False}


def test_registry_port_with_tag():
    result = parse_image_ref("localhost:5000/team/app:1.4")
    assert result["name"] == "localhost:5000/team/app"
    assert result["tag"] == "1.4"


def test_malformed_digest_is_not_pinned():
    assert parse_image_ref("alpine@sha256:abc123")["pinned"] is False
    assert parse_image_ref(f"alpine@sha512:{DIGEST[7:]}")["pinned"] is False
    assert parse_image_ref("alpine@" + DIGEST.upper().replace("SHA256", "sha256"))["pinned"] is False


def test_nested_path_with_digest():
    result = parse_image_ref(f"ghcr.io/org/tools/runner:v2@{DIGEST}")
    assert result["name"] == "ghcr.io/org/tools/runner"
    assert result["tag"] == "v2"
    assert result["pinned"] is True
