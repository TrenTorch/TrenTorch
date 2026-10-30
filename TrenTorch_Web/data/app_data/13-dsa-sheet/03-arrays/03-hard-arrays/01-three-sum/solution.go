package main

import (
	"fmt"
	"sort"
)

// O(n^2) time, O(n) space for the sorted copy and output
func threeSum(nums []int) [][]int {
	a := make([]int, len(nums))
	copy(a, nums)
	sort.Ints(a)
	out := [][]int{}
	for i := 0; i < len(a)-2; i++ {
		if i > 0 && a[i] == a[i-1] {
			continue
		}
		lo, hi := i+1, len(a)-1
		for lo < hi {
			total := a[i] + a[lo] + a[hi]
			switch {
			case total < 0:
				lo++
			case total > 0:
				hi--
			default:
				out = append(out, []int{a[i], a[lo], a[hi]})
				lo++
				hi--
				for lo < hi && a[lo] == a[lo-1] {
					lo++
				}
				for lo < hi && a[hi] == a[hi+1] {
					hi--
				}
			}
		}
	}
	return out
}

func main() {
	fmt.Println(threeSum([]int{-1, 0, 1, 2, -1, -4}))
}
