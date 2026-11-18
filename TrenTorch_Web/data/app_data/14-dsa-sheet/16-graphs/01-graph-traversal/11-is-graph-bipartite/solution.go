package main

import "fmt"

// O(n + E) time, O(n + E) space
func isBipartite(n int, edges [][]int) bool {
	adj := make([][]int, n)
	for _, e := range edges {
		a, b := e[0], e[1]
		adj[a] = append(adj[a], b)
		adj[b] = append(adj[b], a)
	}
	color := make([]int, n)
	for i := range color {
		color[i] = -1
	}
	for start := 0; start < n; start++ {
		if color[start] != -1 {
			continue
		}
		color[start] = 0
		queue := []int{start}
		for head := 0; head < len(queue); head++ {
			node := queue[head]
			for _, nxt := range adj[node] {
				if color[nxt] == -1 {
					color[nxt] = 1 - color[node]
					queue = append(queue, nxt)
				} else if color[nxt] == color[node] {
					return false
				}
			}
		}
	}
	return true
}

func main() {
	fmt.Println(isBipartite(4, [][]int{[]int{0, 1}, []int{1, 2}, []int{2, 3}, []int{3, 0}}))
}
