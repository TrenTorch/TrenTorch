package main

import (
	"fmt"
	"sort"
)

// O(2^n) time and space for the output (plus sorting cost per step), O(2^n) space
func allSubsetSums(nums []int) []int {
	sums := []int{0}
	for _, x := range nums {
		next := make([]int, 0, 2*len(sums))
		for _, s := range sums {
			next = append(next, s)
		}
		for _, s := range sums {
			next = append(next, s+x)
		}
		sort.Ints(next)
		sums = next
	}
	return sums
}

func main() {
	fmt.Println(allSubsetSums([]int{1, 2}))
}
