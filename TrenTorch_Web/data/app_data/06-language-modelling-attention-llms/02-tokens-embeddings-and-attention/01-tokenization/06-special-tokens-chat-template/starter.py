def render_chat(messages: list[dict], add_generation_prompt: bool = False) -> str:
    """Render messages as <|role|>\ncontent<|end|>\n, optionally ending with an open assistant header."""
    # TODO
    pass


def split_on_specials(text: str, specials: list[str]) -> list[str]:
    """Split text so each special token is its own piece (longest match first); other text is kept as pieces."""
    # TODO
    pass
