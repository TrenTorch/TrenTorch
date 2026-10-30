package main

import "fmt"

// O(n^2) time, O(n) space
func minInsertions(s string) int {
	n := len(s)
	if n == 0 {
		return 0
	}
	prev := make([]int, n)
	for i := n - 1; i >= 0; i-- {
		cur := make([]int, n)
		cur[i] = 1
		for j := i + 1; j < n; j++ {
			if s[i] == s[j] {
				cur[j] = 2 + prev[j-1]
			} else {
				cur[j] = max(prev[j], cur[j-1])
			}
		}
		prev = cur
	}
	return n - prev[n-1]
}

func main() {
	fmt.Println(minInsertions("mbadm"))
}
