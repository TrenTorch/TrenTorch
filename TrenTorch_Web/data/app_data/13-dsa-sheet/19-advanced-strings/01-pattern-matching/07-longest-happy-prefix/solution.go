package main

import "fmt"

// O(n) time, O(n) space
func longestHappyPrefix(s string) string {
	n := len(s)
	if n == 0 {
		return ""
	}
	pi := make([]int, n)
	k := 0
	for i := 1; i < n; i++ {
		for k > 0 && s[i] != s[k] {
			k = pi[k-1]
		}
		if s[i] == s[k] {
			k++
		}
		pi[i] = k
	}
	return s[:pi[n-1]]
}

func main() {
	fmt.Println(longestHappyPrefix("level"))
}
