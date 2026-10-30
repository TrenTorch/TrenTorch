package main

import "fmt"

// O(n + E) time, O(n + E) space
func countComponents(n int, edges [][]int) int {
	adj := make([][]int, n)
	for _, e := range edges {
		a, b := e[0], e[1]
		adj[a] = append(adj[a], b)
		adj[b] = append(adj[b], a)
	}
	seen := make([]bool, n)
	count := 0
	for start := 0; start < n; start++ {
		if seen[start] {
			continue
		}
		count++
		seen[start] = true
		stack := []int{start}
		for len(stack) > 0 {
			node := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			for _, nxt := range adj[node] {
				if !seen[nxt] {
					seen[nxt] = true
					stack = append(stack, nxt)
				}
			}
		}
	}
	return count
}

func main() {
	fmt.Println(countComponents(5, [][]int{[]int{0, 1}, []int{1, 2}, []int{3, 4}}))
}
