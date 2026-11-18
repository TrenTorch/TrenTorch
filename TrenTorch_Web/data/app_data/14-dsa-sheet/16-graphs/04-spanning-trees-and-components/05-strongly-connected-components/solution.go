package main

import "fmt"

type sccFrame struct {
	node, i int
}

// O(n + E) time, O(n + E) space
func countScc(n int, edges [][]int) int {
	adj := make([][]int, n)
	rev := make([][]int, n)
	for _, e := range edges {
		a, b := e[0], e[1]
		adj[a] = append(adj[a], b)
		rev[b] = append(rev[b], a)
	}
	seen := make([]bool, n)
	order := []int{}
	for start := 0; start < n; start++ {
		if seen[start] {
			continue
		}
		seen[start] = true
		stack := []sccFrame{{start, 0}}
		for len(stack) > 0 {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			node, i := top.node, top.i
			if i < len(adj[node]) {
				stack = append(stack, sccFrame{node, i + 1})
				nxt := adj[node][i]
				if !seen[nxt] {
					seen[nxt] = true
					stack = append(stack, sccFrame{nxt, 0})
				}
			} else {
				order = append(order, node)
			}
		}
	}
	seen = make([]bool, n)
	count := 0
	for idx := len(order) - 1; idx >= 0; idx-- {
		start := order[idx]
		if seen[start] {
			continue
		}
		count++
		seen[start] = true
		stack := []int{start}
		for len(stack) > 0 {
			node := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			for _, nxt := range rev[node] {
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
	fmt.Println(countScc(5, [][]int{[]int{0, 1}, []int{1, 2}, []int{2, 0}, []int{1, 3}, []int{3, 4}}))
}
