package main

import "fmt"

// O(n) time, O(n) space
func wordPattern(pattern string, words []string) bool {
	if len(pattern) != len(words) {
		return false
	}
	letterToWord := map[byte]string{}
	wordToLetter := map[string]byte{}
	for i := 0; i < len(pattern); i++ {
		letter, word := pattern[i], words[i]
		if mapped, ok := letterToWord[letter]; ok {
			if mapped != word {
				return false
			}
		} else {
			letterToWord[letter] = word
		}
		if mapped, ok := wordToLetter[word]; ok {
			if mapped != letter {
				return false
			}
		} else {
			wordToLetter[word] = letter
		}
	}
	return true
}

func main() {
	fmt.Println(wordPattern("abba", []string{"dog", "cat", "cat", "dog"}))
}
