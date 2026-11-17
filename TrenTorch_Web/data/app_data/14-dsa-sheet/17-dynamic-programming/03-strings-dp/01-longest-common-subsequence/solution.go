package main

import "fmt"

// O(len(a) * len(b)) time, O(min(len(a), len(b))) space
func lcsLength(a string, b string) int {
	if len(b) > len(a) {
		a, b = b, a
	}
	prev := make([]int, len(b)+1)
	for i := 1; i <= len(a); i++ {
		cur := make([]int, len(b)+1)
		for j := 1; j <= len(b); j++ {
			if a[i-1] == b[j-1] {
				cur[j] = prev[j-1] + 1
			} else {
				cur[j] = max(prev[j], cur[j-1])
			}
		}
		prev = cur
	}
	return prev[len(b)]
}

func main() {
	fmt.Println(lcsLength("abcde", "ace"))
}
