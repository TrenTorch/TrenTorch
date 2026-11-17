package main

import (
	"fmt"
	"sort"
)

type cbFrame struct {
	node, parent, i int
}

// O(n + E) time, O(n + E) space
func criticalConnections(n int, connections [][]int) [][]int {
	adj := make([][]int, n)
	for _, c := range connections {
		a, b := c[0], c[1]
		adj[a] = append(adj[a], b)
		adj[b] = append(adj[b], a)
	}
	disc := make([]int, n)
	for i := range disc {
		disc[i] = -1
	}
	low := make([]int, n)
	bridges := [][]int{}
	timer := 0
	for root := 0; root < n; root++ {
		if disc[root] != -1 {
			continue
		}
		disc[root] = timer
		low[root] = timer
		timer++
		stack := []cbFrame{{root, -1, 0}}
		for len(stack) > 0 {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			node, parent, i := top.node, top.parent, top.i
			if i < len(adj[node]) {
				stack = append(stack, cbFrame{node, parent, i + 1})
				nxt := adj[node][i]
				if nxt == parent {
					continue
				}
				if disc[nxt] == -1 {
					disc[nxt] = timer
					low[nxt] = timer
					timer++
					stack = append(stack, cbFrame{nxt, node, 0})
				} else {
					low[node] = min(low[node], disc[nxt])
				}
			} else if parent != -1 {
				low[parent] = min(low[parent], low[node])
				if low[node] > disc[parent] {
					bridges = append(bridges, []int{min(parent, node), max(parent, node)})
				}
			}
		}
	}
	sort.Slice(bridges, func(i, j int) bool {
		if bridges[i][0] != bridges[j][0] {
			return bridges[i][0] < bridges[j][0]
		}
		return bridges[i][1] < bridges[j][1]
	})
	return bridges
}

func main() {
	fmt.Println(criticalConnections(4, [][]int{[]int{0, 1}, []int{1, 2}, []int{2, 0}, []int{1, 3}}))
}
