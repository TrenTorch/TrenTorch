package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space (copy and sort)
func kSmallest(nums []int, k int) []int {
	if k <= 0 {
		return []int{}
	}
	sorted := make([]int, len(nums))
	copy(sorted, nums)
	sort.Ints(sorted)
	if k > len(sorted) {
		k = len(sorted)
	}
	return sorted[:k]
}

func main() {
	fmt.Println(kSmallest([]int{7, 2, 9, 4, 2}, 3))
}
