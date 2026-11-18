package main

import "fmt"

type apFrame struct {
	node, parent, i int
}

// O(n + E) time, O(n + E) space
func articulationPoints(n int, edges [][]int) []int {
	adj := make([][]int, n)
	for _, e := range edges {
		a, b := e[0], e[1]
		adj[a] = append(adj[a], b)
		adj[b] = append(adj[b], a)
	}
	disc := make([]int, n)
	for i := range disc {
		disc[i] = -1
	}
	low := make([]int, n)
	isCut := make([]bool, n)
	timer := 0
	for root := 0; root < n; root++ {
		if disc[root] != -1 {
			continue
		}
		disc[root] = timer
		low[root] = timer
		timer++
		rootChildren := 0
		stack := []apFrame{{root, -1, 0}}
		for len(stack) > 0 {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			node, parent, i := top.node, top.parent, top.i
			if i < len(adj[node]) {
				stack = append(stack, apFrame{node, parent, i + 1})
				nxt := adj[node][i]
				if nxt == parent {
					continue
				}
				if disc[nxt] == -1 {
					disc[nxt] = timer
					low[nxt] = timer
					timer++
					if node == root {
						rootChildren++
					}
					stack = append(stack, apFrame{nxt, node, 0})
				} else {
					low[node] = min(low[node], disc[nxt])
				}
			} else if parent != -1 {
				low[parent] = min(low[parent], low[node])
				if parent != root && low[node] >= disc[parent] {
					isCut[parent] = true
				}
			}
		}
		if rootChildren >= 2 {
			isCut[root] = true
		}
	}
	res := []int{}
	for v := 0; v < n; v++ {
		if isCut[v] {
			res = append(res, v)
		}
	}
	return res
}

func main() {
	fmt.Println(articulationPoints(5, [][]int{[]int{0, 1}, []int{1, 2}, []int{2, 0}, []int{1, 3}, []int{3, 4}}))
}
