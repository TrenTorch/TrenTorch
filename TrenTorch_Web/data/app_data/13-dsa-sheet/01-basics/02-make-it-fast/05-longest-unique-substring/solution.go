package main

import "fmt"

// O(n) time, O(k) space where k is the number of distinct characters (sliding window)
func longestUniqueSubstring(s string) int {
	runes := []rune(s)
	last := make(map[rune]int)
	start, best := 0, 0
	for i, ch := range runes {
		if p, ok := last[ch]; ok && p >= start {
			start = p + 1
		}
		last[ch] = i
		best = max(best, i-start+1)
	}
	return best
}

func main() {
	fmt.Println(longestUniqueSubstring("abcabcbb"))
}
