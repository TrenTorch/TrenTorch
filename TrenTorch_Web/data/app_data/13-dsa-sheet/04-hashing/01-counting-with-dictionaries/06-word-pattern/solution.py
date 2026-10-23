def word_pattern(pattern, words):
    if len(pattern) != len(words):
        return False
    letter_to_word = {}
    word_to_letter = {}
    for letter, word in zip(pattern, words):
        if letter_to_word.setdefault(letter, word) != word:
            return False
        if word_to_letter.setdefault(word, letter) != letter:
            return False
    return True
