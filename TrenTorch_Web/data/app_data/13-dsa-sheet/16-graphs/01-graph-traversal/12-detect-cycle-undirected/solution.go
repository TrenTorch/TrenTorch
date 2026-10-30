package main

import "fmt"

type neighbor struct{ to, id int }

type undirFrame struct{ node, via int }

// O(n + E) time, O(n + E) space
func hasCycleUndirected(n int, edges [][]int) bool {
	adj := make([][]neighbor, n)
	for i, e := range edges {
		a, b := e[0], e[1]
		if a == b {
			return true
		}
		adj[a] = append(adj[a], neighbor{b, i})
		adj[b] = append(adj[b], neighbor{a, i})
	}
	seen := make([]bool, n)
	for start := 0; start < n; start++ {
		if seen[start] {
			continue
		}
		seen[start] = true
		stack := []undirFrame{{start, -1}}
		for len(stack) > 0 {
			cur := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			for _, nb := range adj[cur.node] {
				if nb.id == cur.via {
					continue
				}
				if seen[nb.to] {
					return true
				}
				seen[nb.to] = true
				stack = append(stack, undirFrame{nb.to, nb.id})
			}
		}
	}
	return false
}

func main() {
	fmt.Println(hasCycleUndirected(4, [][]int{[]int{0, 1}, []int{1, 2}, []int{2, 0}, []int{3, 3}}))
}
