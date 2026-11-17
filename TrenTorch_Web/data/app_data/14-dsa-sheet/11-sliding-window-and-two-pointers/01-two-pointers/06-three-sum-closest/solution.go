package main

import (
	"fmt"
	"sort"
)

// O(n^2) time, O(n) space
func threeSumClosest(nums []int, target int) int {
	a := make([]int, len(nums))
	copy(a, nums)
	sort.Ints(a)
	best := a[0] + a[1] + a[2]
	for i := 0; i < len(a)-2; i++ {
		lo, hi := i+1, len(a)-1
		for lo < hi {
			s := a[i] + a[lo] + a[hi]
			diff := absInt(s - target)
			bestDiff := absInt(best - target)
			if diff < bestDiff || (diff == bestDiff && s < best) {
				best = s
			}
			if s < target {
				lo++
			} else if s > target {
				hi--
			} else {
				return s
			}
		}
	}
	return best
}

func absInt(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	fmt.Println(threeSumClosest([]int{-1, 2, 1, -4}, 1))
}
