def decode_bio(tags):
    spans, cur_type, start = [], None, None
    for i, tag in enumerate(tags):
        if tag == "O":
            if cur_type is not None:
                spans.append((cur_type, start, i))
                cur_type = None
            continue
        prefix, typ = tag.split("-", 1)
        if prefix == "I" and cur_type == typ:
            continue
        if cur_type is not None:
            spans.append((cur_type, start, i))
        cur_type, start = typ, i
    if cur_type is not None:
        spans.append((cur_type, start, len(tags)))
    return spans
