package main

import (
	"fmt"
	"sort"
)

// O(n^2) time, O(n) space
func countTripletsSmaller(nums []int, target int) int {
	a := make([]int, len(nums))
	copy(a, nums)
	sort.Ints(a)
	count := 0
	for i := 0; i < len(a)-2; i++ {
		lo, hi := i+1, len(a)-1
		for lo < hi {
			if a[i]+a[lo]+a[hi] < target {
				count += hi - lo
				lo++
			} else {
				hi--
			}
		}
	}
	return count
}

func main() {
	fmt.Println(countTripletsSmaller([]int{-2, 0, 1, 3}, 2))
}
