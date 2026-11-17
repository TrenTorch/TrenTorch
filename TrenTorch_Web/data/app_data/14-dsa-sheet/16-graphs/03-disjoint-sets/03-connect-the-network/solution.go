package main

import "fmt"

// O(n + E * alpha(n)) time, O(n) space
func makeConnected(n int, connections [][]int) int {
	if len(connections) < n-1 {
		return -1
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
	components := n
	for _, c := range connections {
		a, b := c[0], c[1]
		ra, rb := find(a), find(b)
		if ra != rb {
			if size[ra] < size[rb] {
				ra, rb = rb, ra
			}
			parent[rb] = ra
			size[ra] += size[rb]
			components--
		}
	}
	return components - 1
}

func main() {
	fmt.Println(makeConnected(4, [][]int{[]int{0, 1}, []int{0, 2}, []int{1, 2}}))
}
