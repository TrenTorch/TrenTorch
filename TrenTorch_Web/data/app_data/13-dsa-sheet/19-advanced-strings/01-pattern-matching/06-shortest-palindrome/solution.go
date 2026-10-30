package main

import "fmt"

// O(n) time, O(n) space
func shortestPalindrome(s string) string {
	t := s + "#" + reverseString(s)
	n := len(t)
	pi := make([]int, n)
	k := 0
	for i := 1; i < n; i++ {
		for k > 0 && t[i] != t[k] {
			k = pi[k-1]
		}
		if t[i] == t[k] {
			k++
		}
		pi[i] = k
	}
	border := 0
	if n > 0 {
		border = pi[n-1]
	}
	return reverseString(s[border:]) + s
}

func reverseString(s string) string {
	b := []byte(s)
	for i, j := 0, len(b)-1; i < j; i, j = i+1, j-1 {
		b[i], b[j] = b[j], b[i]
	}
	return string(b)
}

func main() {
	fmt.Println(shortestPalindrome("aacecaaa"))
}
