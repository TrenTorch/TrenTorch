package main

import "fmt"

// O(n + E) time, O(n + E) space
func validPath(n int, edges [][]int, source int, destination int) bool {
	adj := make([][]int, n)
	for _, e := range edges {
		a, b := e[0], e[1]
		adj[a] = append(adj[a], b)
		adj[b] = append(adj[b], a)
	}
	seen := make([]bool, n)
	seen[source] = true
	stack := []int{source}
	for len(stack) > 0 {
		node := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if node == destination {
			return true
		}
		for _, nxt := range adj[node] {
			if !seen[nxt] {
				seen[nxt] = true
				stack = append(stack, nxt)
			}
		}
	}
	return false
}

func main() {
	fmt.Println(validPath(3, [][]int{[]int{0, 1}, []int{1, 2}, []int{2, 0}}, 0, 2))
}
