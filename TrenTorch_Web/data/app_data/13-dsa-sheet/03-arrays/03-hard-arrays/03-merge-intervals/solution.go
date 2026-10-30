package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space
func mergeIntervals(intervals [][]int) [][]int {
	ordered := make([][]int, len(intervals))
	copy(ordered, intervals)
	sort.Slice(ordered, func(i, j int) bool {
		if ordered[i][0] != ordered[j][0] {
			return ordered[i][0] < ordered[j][0]
		}
		return ordered[i][1] < ordered[j][1]
	})
	out := [][]int{}
	for _, iv := range ordered {
		start, end := iv[0], iv[1]
		if len(out) > 0 && start <= out[len(out)-1][1] {
			if end > out[len(out)-1][1] {
				out[len(out)-1][1] = end
			}
		} else {
			out = append(out, []int{start, end})
		}
	}
	return out
}

func main() {
	fmt.Println(mergeIntervals([][]int{[]int{1, 3}, []int{8, 10}, []int{2, 6}, []int{15, 18}}))
}
