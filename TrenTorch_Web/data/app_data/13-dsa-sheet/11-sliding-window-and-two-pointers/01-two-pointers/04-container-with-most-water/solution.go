package main

import "fmt"

// O(n) time, O(1) space
func maxWater(heights []int) int {
	left, right := 0, len(heights)-1
	best := 0
	for left < right {
		best = max(best, min(heights[left], heights[right])*(right-left))
		if heights[left] < heights[right] {
			left++
		} else {
			right--
		}
	}
	return best
}

func main() {
	fmt.Println(maxWater([]int{1, 8, 6, 2, 5, 4, 8, 3, 7}))
}
