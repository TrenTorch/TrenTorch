package main

import "fmt"

// O(n) time, O(n) space
func countSubarraysXorK(nums []int, k int) int {
	seen := map[int]int{0: 1}
	prefix, count := 0, 0
	for _, x := range nums {
		prefix ^= x
		count += seen[prefix^k]
		seen[prefix]++
	}
	return count
}

func main() {
	fmt.Println(countSubarraysXorK([]int{4, 2, 2, 6, 4}, 6))
}
