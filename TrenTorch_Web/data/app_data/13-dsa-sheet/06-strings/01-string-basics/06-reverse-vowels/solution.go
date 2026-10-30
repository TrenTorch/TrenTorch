package main

import "fmt"

func isVowel(c rune) bool {
	switch c {
	case 'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U':
		return true
	}
	return false
}

// O(n) time, O(n) space
func reverseVowels(s string) string {
	r := []rune(s)
	i, j := 0, len(r)-1
	for i < j {
		for i < j && !isVowel(r[i]) {
			i++
		}
		for i < j && !isVowel(r[j]) {
			j--
		}
		if i < j {
			r[i], r[j] = r[j], r[i]
			i++
			j--
		}
	}
	return string(r)
}

func main() {
	fmt.Println(reverseVowels("hello"))
}
