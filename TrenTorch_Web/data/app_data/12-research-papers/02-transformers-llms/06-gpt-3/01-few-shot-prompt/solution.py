def build_few_shot_prompt(examples, query, sep="\n\n"):
    parts = [f"{x} => {y}" for x, y in examples] + [f"{query} =>"]
    return sep.join(parts)
