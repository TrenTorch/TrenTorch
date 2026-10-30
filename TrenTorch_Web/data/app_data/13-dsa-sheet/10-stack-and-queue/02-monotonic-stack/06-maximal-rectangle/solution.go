package main

import "fmt"

// O(rows*cols) time, O(cols) space
func maximalRectangle(matrix [][]int) int {
	if len(matrix) == 0 {
		return 0
	}
	cols := len(matrix[0])
	heights := make([]int, cols)
	best := 0
	for _, row := range matrix {
		for j := 0; j < cols; j++ {
			if row[j] != 0 {
				heights[j]++
			} else {
				heights[j] = 0
			}
		}
		best = max(best, largestInHistogram(heights))
	}
	return best
}

// largestInHistogram runs the monotonic-stack histogram scan in O(len(hs)) time.
func largestInHistogram(hs []int) int {
	result := 0
	stack := []int{}
	for i := 0; i <= len(hs); i++ {
		h := 0
		if i < len(hs) {
			h = hs[i]
		}
		for len(stack) > 0 && hs[stack[len(stack)-1]] >= h {
			height := hs[stack[len(stack)-1]]
			stack = stack[:len(stack)-1]
			left := -1
			if len(stack) > 0 {
				left = stack[len(stack)-1]
			}
			result = max(result, height*(i-left-1))
		}
		stack = append(stack, i)
	}
	return result
}

func main() {
	fmt.Println(maximalRectangle([][]int{[]int{1, 0, 1, 0, 0}, []int{1, 0, 1, 1, 1}, []int{1, 1, 1, 1, 1}, []int{1, 0, 0, 1, 0}}))
}
