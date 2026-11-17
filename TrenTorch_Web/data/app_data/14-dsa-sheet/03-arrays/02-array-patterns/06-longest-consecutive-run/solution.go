package main

import "fmt"

// O(n) time, O(n) space
func longestConsecutive(nums []int) int {
	values := make(map[int]bool, len(nums))
	for _, x := range nums {
		values[x] = true
	}
	best := 0
	for x := range values {
		if !values[x-1] {
			length := 1
			for values[x+length] {
				length++
			}
			best = max(best, length)
		}
	}
	return best
}

func main() {
	fmt.Println(longestConsecutive([]int{100, 4, 200, 1, 3, 2}))
}
