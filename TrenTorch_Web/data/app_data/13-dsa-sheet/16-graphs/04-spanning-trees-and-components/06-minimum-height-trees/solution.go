package main

import (
	"fmt"
	"sort"
)

// O(n) time, O(n) space
func minHeightTrees(n int, edges [][]int) []int {
	if n <= 2 {
		res := make([]int, n)
		for i := range res {
			res[i] = i
		}
		return res
	}
	adj := make([][]int, n)
	for _, e := range edges {
		a, b := e[0], e[1]
		adj[a] = append(adj[a], b)
		adj[b] = append(adj[b], a)
	}
	degree := make([]int, n)
	for v := range adj {
		degree[v] = len(adj[v])
	}
	leaves := []int{}
	for v := 0; v < n; v++ {
		if degree[v] == 1 {
			leaves = append(leaves, v)
		}
	}
	remaining := n
	for remaining > 2 {
		remaining -= len(leaves)
		nxt := []int{}
		for _, leaf := range leaves {
			for _, other := range adj[leaf] {
				degree[other]--
				if degree[other] == 1 {
					nxt = append(nxt, other)
				}
			}
		}
		leaves = nxt
	}
	sort.Ints(leaves)
	return leaves
}

func main() {
	fmt.Println(minHeightTrees(6, [][]int{[]int{3, 0}, []int{3, 1}, []int{3, 2}, []int{3, 4}, []int{5, 4}}))
}
