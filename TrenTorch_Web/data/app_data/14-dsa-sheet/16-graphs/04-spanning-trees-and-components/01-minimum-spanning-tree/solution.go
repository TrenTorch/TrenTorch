package main

import (
	"fmt"
	"sort"
)

// O(E log E) time, O(n + E) space
func mstWeight(n int, edges [][]int) int {
	parent := make([]int, n)
	size := make([]int, n)
	for i := range parent {
		parent[i] = i
		size[i] = 1
	}
	find := func(a int) int {
		for parent[a] != a {
			parent[a] = parent[parent[a]]
			a = parent[a]
		}
		return a
	}
	sorted := make([][]int, len(edges))
	copy(sorted, edges)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i][2] < sorted[j][2] })
	total := 0
	taken := 0
	for _, e := range sorted {
		a, b, w := e[0], e[1], e[2]
		ra, rb := find(a), find(b)
		if ra != rb {
			if size[ra] < size[rb] {
				ra, rb = rb, ra
			}
			parent[rb] = ra
			size[ra] += size[rb]
			total += w
			taken++
		}
	}
	if taken == n-1 {
		return total
	}
	return -1
}

func main() {
	fmt.Println(mstWeight(4, [][]int{[]int{0, 1, 1}, []int{1, 2, 2}, []int{2, 3, 3}, []int{0, 3, 10}, []int{0, 2, 5}}))
}
