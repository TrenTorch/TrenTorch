package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space
func maxActivities(starts []int, ends []int) int {
	idx := make([]int, len(starts))
	for i := range idx {
		idx[i] = i
	}
	sort.Slice(idx, func(a, b int) bool {
		i, j := idx[a], idx[b]
		if ends[i] != ends[j] {
			return ends[i] < ends[j]
		}
		return starts[i] < starts[j]
	})
	count := 0
	lastEnd := -1
	for _, k := range idx {
		if starts[k] >= lastEnd {
			count++
			lastEnd = ends[k]
		}
	}
	return count
}

func main() {
	fmt.Println(maxActivities([]int{1, 3, 0, 5, 8, 5}, []int{2, 4, 6, 7, 9, 9}))
}
