def render_chat(messages, add_generation_prompt=False):
    out = "".join(f"<|{m['role']}|>\n{m['content']}<|end|>\n" for m in messages)
    if add_generation_prompt:
        out += "<|assistant|>\n"
    return out


def split_on_specials(text, specials):
    ordered = sorted(specials, key=len, reverse=True)
    pieces, buf, i = [], [], 0
    while i < len(text):
        match = next((s for s in ordered if s and text.startswith(s, i)), None)
        if match is None:
            buf.append(text[i])
            i += 1
        else:
            if buf:
                pieces.append("".join(buf))
                buf = []
            pieces.append(match)
            i += len(match)
    if buf:
        pieces.append("".join(buf))
    return pieces
