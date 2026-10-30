package main

import "fmt"

// O(n) time, O(1) space
func majorityElement(nums []int) int {
	candidate := 0
	count := 0
	for _, x := range nums {
		if count == 0 {
			candidate = x
		}
		if x == candidate {
			count++
		} else {
			count--
		}
	}
	occurrences := 0
	for _, x := range nums {
		if x == candidate {
			occurrences++
		}
	}
	if len(nums) > 0 && occurrences > len(nums)/2 {
		return candidate
	}
	return -1
}

func main() {
	fmt.Println(majorityElement([]int{2, 2, 1, 1, 2, 2, 3}))
}
