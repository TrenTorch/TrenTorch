package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space
func lengthOfLis(nums []int) int {
	tails := []int{}
	for _, x := range nums {
		i := sort.SearchInts(tails, x)
		if i == len(tails) {
			tails = append(tails, x)
		} else {
			tails[i] = x
		}
	}
	return len(tails)
}

func main() {
	fmt.Println(lengthOfLis([]int{10, 9, 2, 5, 3, 7, 101, 18}))
}
