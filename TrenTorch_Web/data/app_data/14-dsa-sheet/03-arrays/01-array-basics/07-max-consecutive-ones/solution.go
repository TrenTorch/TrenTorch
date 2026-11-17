package main

import "fmt"

// O(n) time, O(1) space
func maxConsecutiveOnes(nums []int) int {
	best, current := 0, 0
	for _, x := range nums {
		if x == 1 {
			current++
			best = max(best, current)
		} else {
			current = 0
		}
	}
	return best
}

func main() {
	fmt.Println(maxConsecutiveOnes([]int{1, 1, 0, 1, 1, 1}))
}
