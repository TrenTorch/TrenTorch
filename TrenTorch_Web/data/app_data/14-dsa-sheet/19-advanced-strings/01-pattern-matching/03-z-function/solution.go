package main

import "fmt"

// O(n) time, O(n) space
func zFunction(s string) []int {
	n := len(s)
	z := make([]int, n)
	left, right := 0, 0
	for i := 1; i < n; i++ {
		if i < right {
			z[i] = min(right-i, z[i-left])
		}
		for i+z[i] < n && s[z[i]] == s[i+z[i]] {
			z[i]++
		}
		if i+z[i] > right {
			left, right = i, i+z[i]
		}
	}
	return z
}

func main() {
	fmt.Println(zFunction("aabxaab"))
}
