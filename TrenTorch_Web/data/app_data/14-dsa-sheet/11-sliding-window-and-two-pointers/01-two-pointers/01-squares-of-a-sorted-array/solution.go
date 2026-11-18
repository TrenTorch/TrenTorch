package main

import "fmt"

// O(n) time, O(n) space
func sortedSquares(nums []int) []int {
	n := len(nums)
	out := make([]int, n)
	left, right := 0, n-1
	for i := n - 1; i >= 0; i-- {
		if nums[left]*nums[left] > nums[right]*nums[right] {
			out[i] = nums[left] * nums[left]
			left++
		} else {
			out[i] = nums[right] * nums[right]
			right--
		}
	}
	return out
}

func main() {
	fmt.Println(sortedSquares([]int{-4, -1, 0, 3, 10}))
}
