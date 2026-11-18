package main

import "fmt"

// O(n) time, O(u) space where u is the number of distinct characters
func isAnagram(a string, b string) bool {
	if len(a) != len(b) {
		return false
	}
	counts := make(map[rune]int)
	for _, ch := range a {
		counts[ch]++
	}
	for _, ch := range b {
		counts[ch]--
		if counts[ch] < 0 {
			return false
		}
	}
	return true
}

func main() {
	fmt.Println(isAnagram("listen", "silent"))
}
