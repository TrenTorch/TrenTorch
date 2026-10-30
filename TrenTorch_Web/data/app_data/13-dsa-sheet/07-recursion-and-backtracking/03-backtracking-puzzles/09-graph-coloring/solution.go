package main

import "fmt"

// O(colors^n * (n + m)) worst-case time, O(n + m) space
func canColorGraph(n int, edges [][]int, colors int) bool {
	for _, e := range edges {
		if e[0] == e[1] {
			return false
		}
	}
	adj := make([][]int, n)
	for _, e := range edges {
		u, v := e[0], e[1]
		adj[u] = append(adj[u], v)
		adj[v] = append(adj[v], u)
	}
	color := make([]int, n)
	for i := range color {
		color[i] = -1
	}
	var rec func(i int) bool
	rec = func(i int) bool {
		if i == n {
			return true
		}
		for c := 0; c < colors; c++ {
			ok := true
			for _, j := range adj[i] {
				if color[j] == c {
					ok = false
					break
				}
			}
			if ok {
				color[i] = c
				if rec(i + 1) {
					return true
				}
				color[i] = -1
			}
		}
		return false
	}
	return rec(0)
}

func main() {
	fmt.Println(canColorGraph(3, [][]int{[]int{0, 1}, []int{1, 2}, []int{0, 2}}, 3))
}
