package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space
func jobScheduling(jobs [][]int) int {
	items := make([][]int, len(jobs))
	copy(items, jobs)
	sort.SliceStable(items, func(a, b int) bool { return items[a][1] < items[b][1] })
	n := len(items)
	ends := make([]int, n)
	for i, j := range items {
		ends[i] = j[1]
	}
	best := make([]int, n+1)
	for i := 1; i <= n; i++ {
		start, profit := items[i-1][0], items[i-1][2]
		// bisect_right(ends, start, 0, i-1)
		lo, hi := 0, i-1
		for lo < hi {
			mid := (lo + hi) / 2
			if ends[mid] <= start {
				lo = mid + 1
			} else {
				hi = mid
			}
		}
		best[i] = best[i-1]
		if v := profit + best[lo]; v > best[i] {
			best[i] = v
		}
	}
	return best[n]
}

func main() {
	fmt.Println(jobScheduling([][]int{[]int{1, 3, 50}, []int{2, 4, 10}, []int{3, 5, 40}, []int{3, 6, 70}}))
}
