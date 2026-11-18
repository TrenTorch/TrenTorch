import re


def extract_final_answer(text):
    found = re.findall(r"The answer is\s*([^\.\n]+)", text)
    return found[-1].strip() if found else None
