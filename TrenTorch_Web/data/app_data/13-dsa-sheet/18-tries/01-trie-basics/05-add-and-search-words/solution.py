def run_word_dictionary(ops):
    root = {}
    out = []
    for op in ops:
        kind, text = op.split()
        if kind == "add":
            node = root
            for ch in text:
                node = node.setdefault(ch, {})
            node["$"] = True
        else:

            def go(node, i):
                if i == len(text):
                    return "$" in node
                ch = text[i]
                if ch == ".":
                    return any(
                        go(child, i + 1) for key, child in node.items() if key != "$"
                    )
                return ch in node and go(node[ch], i + 1)

            out.append(go(root, 0))
    return out
