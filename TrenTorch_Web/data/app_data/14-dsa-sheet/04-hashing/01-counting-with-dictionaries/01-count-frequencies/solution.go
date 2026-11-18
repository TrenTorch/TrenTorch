package main

import "fmt"

// O(n + q) time, O(n) space
func countFrequencies(nums []int, queries []int) []int {
	counts := make(map[int]int, len(nums))
	for _, x := range nums {
		counts[x]++
	}
	out := make([]int, len(queries))
	for i, q := range queries {
		out[i] = counts[q]
	}
	return out
}

func main() {
	fmt.Println(countFrequencies([]int{1, 2, 2, 3, 3, 3}, []int{3, 2, 5}))
}
