package main

import "fmt"

// O(n) time, O(k) space
func subarraysDivisibleByK(nums []int, k int) int {
	seen := map[int]int{0: 1}
	prefix, count := 0, 0
	for _, x := range nums {
		prefix = (prefix + x) % k
		if prefix < 0 {
			prefix += k
		}
		count += seen[prefix]
		seen[prefix]++
	}
	return count
}

func main() {
	fmt.Println(subarraysDivisibleByK([]int{4, 5, 0, -2, -3, 1}, 5))
}
