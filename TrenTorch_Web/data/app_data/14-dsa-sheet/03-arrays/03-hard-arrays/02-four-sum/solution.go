package main

import (
	"fmt"
	"sort"
)

// O(n^3) time, O(n) space for the sorted copy and output
func fourSum(nums []int, target int) [][]int {
	a := make([]int, len(nums))
	copy(a, nums)
	sort.Ints(a)
	n := len(a)
	out := [][]int{}
	for i := 0; i < n-3; i++ {
		if i > 0 && a[i] == a[i-1] {
			continue
		}
		for j := i + 1; j < n-2; j++ {
			if j > i+1 && a[j] == a[j-1] {
				continue
			}
			lo, hi := j+1, n-1
			for lo < hi {
				total := a[i] + a[j] + a[lo] + a[hi]
				switch {
				case total < target:
					lo++
				case total > target:
					hi--
				default:
					out = append(out, []int{a[i], a[j], a[lo], a[hi]})
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
	}
	return out
}

func main() {
	fmt.Println(fourSum([]int{1, 0, -1, 0, -2, 2}, 0))
}
