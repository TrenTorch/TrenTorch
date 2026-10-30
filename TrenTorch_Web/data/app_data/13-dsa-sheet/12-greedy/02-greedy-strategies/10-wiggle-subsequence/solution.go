package main

import "fmt"

// O(n) time, O(1) space
func wiggleLength(nums []int) int {
	if len(nums) == 0 {
		return 0
	}
	length := 1
	direction := 0
	for i := 1; i < len(nums); i++ {
		diff := nums[i] - nums[i-1]
		if diff > 0 && direction <= 0 {
			length++
			direction = 1
		} else if diff < 0 && direction >= 0 {
			length++
			direction = -1
		}
	}
	return length
}

func main() {
	fmt.Println(wiggleLength([]int{1, 7, 4, 9, 2, 5}))
}
