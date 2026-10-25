def ransom_note(note, magazine):
    return all(note.count(ch) <= magazine.count(ch) for ch in set(note))
