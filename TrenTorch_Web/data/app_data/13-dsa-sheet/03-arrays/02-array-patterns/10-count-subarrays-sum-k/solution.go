package main

import "fmt"

// O(n) time, O(n) space
func countSubarraysSumK(nums []int, k int) int {
	seen := map[int]int{0: 1}
	prefix, count := 0, 0
	for _, x := range nums {
		prefix += x
		count += seen[prefix-k]
		seen[prefix]++
	}
	return count
}

func main() {
	fmt.Println(countSubarraysSumK([]int{1, 1, 1}, 2))
}
