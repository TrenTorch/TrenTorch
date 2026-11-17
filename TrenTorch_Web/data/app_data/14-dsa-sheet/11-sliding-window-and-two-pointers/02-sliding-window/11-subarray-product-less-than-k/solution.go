package main

import "fmt"

// O(n) time, O(1) space
func countProductLess(nums []int, k int) int {
	product := 1
	left := 0
	total := 0
	for right, x := range nums {
		product *= x
		for left <= right && product >= k {
			product /= nums[left]
			left++
		}
		total += right - left + 1
	}
	return total
}

func main() {
	fmt.Println(countProductLess([]int{10, 5, 2, 6}, 100))
}
