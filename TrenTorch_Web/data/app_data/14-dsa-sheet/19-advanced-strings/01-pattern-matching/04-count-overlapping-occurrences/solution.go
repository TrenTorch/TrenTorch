package main

import "fmt"

// O(T + P) time, O(P) space (KMP)
func countOverlapping(text string, pattern string) int {
	m := len(pattern)
	fail := make([]int, m)
	k := 0
	for i := 1; i < m; i++ {
		for k > 0 && pattern[i] != pattern[k] {
			k = fail[k-1]
		}
		if pattern[i] == pattern[k] {
			k++
		}
		fail[i] = k
	}
	count := 0
	k = 0
	for i := 0; i < len(text); i++ {
		ch := text[i]
		for k > 0 && ch != pattern[k] {
			k = fail[k-1]
		}
		if ch == pattern[k] {
			k++
		}
		if k == m {
			count++
			k = fail[k-1]
		}
	}
	return count
}

func main() {
	fmt.Println(countOverlapping("aaaa", "aa"))
}
