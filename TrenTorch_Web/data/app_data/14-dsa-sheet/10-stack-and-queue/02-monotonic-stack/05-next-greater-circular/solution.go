package main

import "fmt"

// O(n) time, O(n) space
func nextGreaterCircular(nums []int) []int {
	n := len(nums)
	out := make([]int, n)
	for i := range out {
		out[i] = -1
	}
	stack := []int{}
	for i := 0; i < 2*n; i++ {
		x := nums[i%n]
		for len(stack) > 0 && nums[stack[len(stack)-1]] < x {
			out[stack[len(stack)-1]] = x
			stack = stack[:len(stack)-1]
		}
		if i < n {
			stack = append(stack, i)
		}
	}
	return out
}

func main() {
	fmt.Println(nextGreaterCircular([]int{1, 2, 1}))
}
