package main

import "fmt"

// O(E * alpha(E)) time, O(E) space
func findRedundantConnection(edges [][]int) []int {
	n := len(edges) + 2
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
	for _, e := range edges {
		a, b := e[0], e[1]
		ra, rb := find(a), find(b)
		if ra == rb {
			return []int{a, b}
		}
		if size[ra] < size[rb] {
			ra, rb = rb, ra
		}
		parent[rb] = ra
		size[ra] += size[rb]
	}
	return []int{}
}

func main() {
	fmt.Println(findRedundantConnection([][]int{[]int{1, 2}, []int{1, 3}, []int{2, 3}}))
}
