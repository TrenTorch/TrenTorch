package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space
func minArrows(points [][]int) int {
	sorted := make([][]int, len(points))
	copy(sorted, points)
	sort.SliceStable(sorted, func(a, b int) bool {
		return sorted[a][1] < sorted[b][1]
	})
	arrows := 0
	started := false
	arrow := 0
	for _, p := range sorted {
		start, end := p[0], p[1]
		if !started || start > arrow {
			arrows++
			arrow = end
			started = true
		}
	}
	return arrows
}

func main() {
	fmt.Println(minArrows([][]int{[]int{10, 16}, []int{2, 8}, []int{1, 6}, []int{7, 12}}))
}
