package main

import "fmt"

type dirFrame struct{ node, i int }

// O(n + E) time, O(n + E) space
func hasCycleDirected(n int, edges [][]int) bool {
	adj := make([][]int, n)
	for _, e := range edges {
		adj[e[0]] = append(adj[e[0]], e[1])
	}
	state := make([]int, n)
	for start := 0; start < n; start++ {
		if state[start] != 0 {
			continue
		}
		state[start] = 1
		stack := []dirFrame{{start, 0}}
		for len(stack) > 0 {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			if top.i < len(adj[top.node]) {
				stack = append(stack, dirFrame{top.node, top.i + 1})
				nxt := adj[top.node][top.i]
				if state[nxt] == 1 {
					return true
				}
				if state[nxt] == 0 {
					state[nxt] = 1
					stack = append(stack, dirFrame{nxt, 0})
				}
			} else {
				state[top.node] = 2
			}
		}
	}
	return false
}

func main() {
	fmt.Println(hasCycleDirected(3, [][]int{[]int{0, 1}, []int{1, 2}, []int{2, 0}}))
}
