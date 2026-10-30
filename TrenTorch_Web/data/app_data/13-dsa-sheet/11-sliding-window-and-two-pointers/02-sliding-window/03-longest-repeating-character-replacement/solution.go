package main

import "fmt"

// O(n) time, O(1) space (alphabet bounded by 256 byte values)
func characterReplacement(s string, k int) int {
	var count [256]int
	left := 0
	maxCount := 0
	for right := 0; right < len(s); right++ {
		count[s[right]]++
		if count[s[right]] > maxCount {
			maxCount = count[s[right]]
		}
		if right-left+1-maxCount > k {
			count[s[left]]--
			left++
		}
	}
	return len(s) - left
}

func main() {
	fmt.Println(characterReplacement("AABABBA", 1))
}
