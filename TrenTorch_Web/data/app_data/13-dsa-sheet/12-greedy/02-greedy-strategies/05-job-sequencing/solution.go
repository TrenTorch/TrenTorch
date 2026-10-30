package main

import (
	"fmt"
	"sort"
)

// O(n log n + n*alpha(n)) time, O(n) space
func maxJobProfit(jobs [][]int) int {
	maxDeadline := 0
	for _, j := range jobs {
		if j[0] > maxDeadline {
			maxDeadline = j[0]
		}
	}
	limit := maxDeadline
	if len(jobs) < limit {
		limit = len(jobs)
	}
	parent := make([]int, limit+1)
	for i := range parent {
		parent[i] = i
	}
	find := func(t int) int {
		for parent[t] != t {
			parent[t] = parent[parent[t]]
			t = parent[t]
		}
		return t
	}

	sorted := make([][]int, len(jobs))
	copy(sorted, jobs)
	sort.SliceStable(sorted, func(a, b int) bool {
		return sorted[a][1] > sorted[b][1]
	})

	total := 0
	for _, j := range sorted {
		deadline, profit := j[0], j[1]
		if deadline > limit {
			deadline = limit
		}
		slot := find(deadline)
		if slot > 0 {
			parent[slot] = slot - 1
			total += profit
		}
	}
	return total
}

func main() {
	fmt.Println(maxJobProfit([][]int{[]int{4, 20}, []int{1, 10}, []int{1, 40}, []int{1, 30}}))
}
