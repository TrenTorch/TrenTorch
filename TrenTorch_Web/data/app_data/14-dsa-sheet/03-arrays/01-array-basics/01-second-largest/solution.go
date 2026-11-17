package main

import "fmt"

// O(n) time, O(1) space (single pass tracking the two largest distinct values).
func secondLargest(nums []int) int {
	hasLargest, hasSecond := false, false
	largest, second := 0, 0
	for _, x := range nums {
		if !hasLargest || x > largest {
			second, hasSecond = largest, hasLargest
			largest, hasLargest = x, true
		} else if x < largest && (!hasSecond || x > second) {
			second, hasSecond = x, true
		}
	}
	if !hasSecond {
		return -1
	}
	return second
}

func main() {
	fmt.Println(secondLargest([]int{4, 9, 9, 6}))
}
