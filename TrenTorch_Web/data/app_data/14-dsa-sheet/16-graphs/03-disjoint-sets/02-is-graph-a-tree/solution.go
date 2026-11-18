package main

import "fmt"

// O(n + E * alpha(n)) time, O(n) space
func validTree(n int, edges [][]int) bool {
	if n == 0 || len(edges) != n-1 {
		return false
	}
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
			return false
		}
		if size[ra] < size[rb] {
			ra, rb = rb, ra
		}
		parent[rb] = ra
		size[ra] += size[rb]
	}
	return true
}

func main() {
	fmt.Println(validTree(5, [][]int{[]int{0, 1}, []int{0, 2}, []int{0, 3}, []int{1, 4}}))
}
