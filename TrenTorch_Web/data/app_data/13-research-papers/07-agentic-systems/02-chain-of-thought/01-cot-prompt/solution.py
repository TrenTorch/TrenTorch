def build_cot_prompt(examples, question):
    blocks = [f"Q: {q}\nA: {r} The answer is {a}." for q, r, a in examples]
    blocks.append(f"Q: {question}\nA:")
    return "\n\n".join(blocks)
