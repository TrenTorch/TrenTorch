package main

import "fmt"

// O(n) time, O(n) space
func largestRectangle(heights []int) int {
	n := len(heights)
	best := 0
	stack := []int{}
	for i := 0; i <= n; i++ {
		h := 0
		if i < n {
			h = heights[i]
		}
		for len(stack) > 0 && heights[stack[len(stack)-1]] >= h {
			height := heights[stack[len(stack)-1]]
			stack = stack[:len(stack)-1]
			left := -1
			if len(stack) > 0 {
				left = stack[len(stack)-1]
			}
			best = max(best, height*(i-left-1))
		}
		stack = append(stack, i)
	}
	return best
}

func main() {
	fmt.Println(largestRectangle([]int{2, 1, 5, 6, 2, 3}))
}
