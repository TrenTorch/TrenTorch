package main

import "fmt"

// O(n) time, O(1) space
func firstUniqueCharacter(s string) int {
	var counts [256]int
	for i := 0; i < len(s); i++ {
		counts[s[i]]++
	}
	for i := 0; i < len(s); i++ {
		if counts[s[i]] == 1 {
			return i
		}
	}
	return -1
}

func main() {
	fmt.Println(firstUniqueCharacter("leetcode"))
}
