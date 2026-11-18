package main

import "fmt"

// O(n) time, O(n) space
func prefixFunction(s string) []int {
	pi := make([]int, len(s))
	k := 0
	for i := 1; i < len(s); i++ {
		for k > 0 && s[i] != s[k] {
			k = pi[k-1]
		}
		if s[i] == s[k] {
			k++
		}
		pi[i] = k
	}
	return pi
}

func main() {
	fmt.Println(prefixFunction("abcabca"))
}
