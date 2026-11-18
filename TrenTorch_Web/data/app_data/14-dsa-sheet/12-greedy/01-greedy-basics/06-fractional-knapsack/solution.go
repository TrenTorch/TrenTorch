package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space
func fractionalKnapsack(items [][]int, capacity int) float64 {
	sorted := make([][]int, len(items))
	copy(sorted, items)
	// Compare value/weight ratios by cross-multiplication (weights are positive).
	sort.SliceStable(sorted, func(a, b int) bool {
		return sorted[a][0]*sorted[b][1] > sorted[b][0]*sorted[a][1]
	})
	total := 0.0
	for _, it := range sorted {
		value, weight := it[0], it[1]
		take := weight
		if capacity < take {
			take = capacity
		}
		total += float64(value*take) / float64(weight)
		capacity -= take
		if capacity == 0 {
			break
		}
	}
	return total
}

func main() {
	fmt.Println(fractionalKnapsack([][]int{[]int{60, 10}, []int{100, 20}, []int{120, 30}}, 50))
}
