package main

import "fmt"

// O(n) time, O(n) space
func nextGreater(nums []int) []int {
	out := make([]int, len(nums))
	for i := range out {
		out[i] = -1
	}
	stack := []int{}
	for i, x := range nums {
		for len(stack) > 0 && nums[stack[len(stack)-1]] < x {
			out[stack[len(stack)-1]] = x
			stack = stack[:len(stack)-1]
		}
		stack = append(stack, i)
	}
	return out
}

func main() {
	fmt.Println(nextGreater([]int{2, 1, 2, 4, 3}))
}
