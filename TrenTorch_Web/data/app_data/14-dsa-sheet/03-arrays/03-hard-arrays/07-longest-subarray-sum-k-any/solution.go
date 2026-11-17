package main

import "fmt"

// O(n) time, O(n) space
func longestSubarraySumKAny(nums []int, k int) int {
	first := map[int]int{0: -1}
	prefix, best := 0, 0
	for i, x := range nums {
		prefix += x
		if j, ok := first[prefix-k]; ok {
			best = max(best, i-j)
		}
		if _, ok := first[prefix]; !ok {
			first[prefix] = i
		}
	}
	return best
}

func main() {
	fmt.Println(longestSubarraySumKAny([]int{1, -1, 5, -2, 3}, 3))
}
