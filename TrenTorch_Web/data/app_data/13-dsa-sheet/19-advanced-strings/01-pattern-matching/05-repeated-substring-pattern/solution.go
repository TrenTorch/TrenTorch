package main

import "fmt"

// O(n) time, O(n) space
func repeatedSubstringPattern(s string) bool {
	n := len(s)
	if n < 2 {
		return false
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
	period := n - pi[n-1]
	return pi[n-1] > 0 && n%period == 0
}

func main() {
	fmt.Println(repeatedSubstringPattern("abab"))
}
