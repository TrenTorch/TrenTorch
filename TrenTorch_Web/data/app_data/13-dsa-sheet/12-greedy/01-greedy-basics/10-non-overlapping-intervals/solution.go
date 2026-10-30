package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space
func eraseOverlap(intervals [][]int) int {
	sorted := make([][]int, len(intervals))
	copy(sorted, intervals)
	sort.SliceStable(sorted, func(a, b int) bool {
		return sorted[a][1] < sorted[b][1]
	})
	removed := 0
	lastEnd := 0
	started := false
	for _, it := range sorted {
		start, end := it[0], it[1]
		if !started || start >= lastEnd {
			lastEnd = end
			started = true
		} else {
			removed++
		}
	}
	return removed
}

func main() {
	fmt.Println(eraseOverlap([][]int{[]int{1, 2}, []int{2, 3}, []int{3, 4}, []int{1, 3}}))
}
