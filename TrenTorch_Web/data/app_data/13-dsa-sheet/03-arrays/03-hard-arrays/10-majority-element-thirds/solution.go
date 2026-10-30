package main

import (
	"fmt"
	"sort"
)

// O(n) time, O(1) extra space
func majorityElementThirds(nums []int) []int {
	var a, b, ca, cb int
	hasA, hasB := false, false
	for _, x := range nums {
		if hasA && x == a {
			ca++
		} else if hasB && x == b {
			cb++
		} else if ca == 0 {
			a, ca, hasA = x, 1, true
		} else if cb == 0 {
			b, cb, hasB = x, 1, true
		} else {
			ca--
			cb--
		}
	}
	n := len(nums)
	out := []int{}
	if hasA && countOf(nums, a)*3 > n {
		out = append(out, a)
	}
	if hasB && countOf(nums, b)*3 > n {
		out = append(out, b)
	}
	sort.Ints(out)
	return out
}

func countOf(nums []int, v int) int {
	c := 0
	for _, x := range nums {
		if x == v {
			c++
		}
	}
	return c
}

func main() {
	fmt.Println(majorityElementThirds([]int{3, 2, 3}))
}
