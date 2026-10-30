package main

import "fmt"

// O(len(t)) time, O(1) space
func isSubsequence(s string, t string) bool {
	i := 0
	for j := 0; j < len(t); j++ {
		if i < len(s) && s[i] == t[j] {
			i++
		}
	}
	return i == len(s)
}

func main() {
	fmt.Println(isSubsequence("ace", "abcde"))
}
