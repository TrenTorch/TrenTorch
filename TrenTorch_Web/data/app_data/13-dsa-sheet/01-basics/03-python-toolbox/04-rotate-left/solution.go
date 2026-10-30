package main

import "fmt"

// O(n) time, O(n) space (new list is returned, input is not modified)
func rotateLeft(nums []int, k int) []int {
	if len(nums) == 0 {
		return []int{}
	}
	k %= len(nums)
	out := make([]int, 0, len(nums))
	out = append(out, nums[k:]...)
	out = append(out, nums[:k]...)
	return out
}

func main() {
	fmt.Println(rotateLeft([]int{1, 2, 3, 4, 5}, 2))
}
