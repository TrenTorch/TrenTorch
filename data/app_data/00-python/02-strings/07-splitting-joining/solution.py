def word_count(text: str) -> int:
    return len(text.split())


def reverse_word_order(text: str) -> str:
    words = text.split()
    return " ".join(words[::-1])


def last_field(line: str, sep: str) -> str:
    return line.rsplit(sep, 1)[-1]


def count_nonblank_lines(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip() != "")


def make_csv_line(fields) -> str:
    processed = [f'"{field}"' if "," in field else field for field in fields]
    return ",".join(processed)
