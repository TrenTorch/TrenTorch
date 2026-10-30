package main

import "fmt"

// O(n) time, O(n) space
func hasDuplicate(nums []int) bool {
	seen := make(map[int]struct{}, len(nums))
	for _, x := range nums {
		if _, ok := seen[x]; ok {
			return true
		}
		seen[x] = struct{}{}
	}
	return false
}

func main() {
	fmt.Println(hasDuplicate([]int{1, 2, 3, 1}))
}
