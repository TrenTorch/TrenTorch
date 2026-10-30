package main

import "fmt"

// O(n) time, O(1) space
func trapWater(heights []int) int {
	left, right := 0, len(heights)-1
	leftMax, rightMax := 0, 0
	total := 0
	for left < right {
		if heights[left] < heights[right] {
			if heights[left] > leftMax {
				leftMax = heights[left]
			}
			total += leftMax - heights[left]
			left++
		} else {
			if heights[right] > rightMax {
				rightMax = heights[right]
			}
			total += rightMax - heights[right]
			right--
		}
	}
	return total
}

func main() {
	fmt.Println(trapWater([]int{0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1}))
}
