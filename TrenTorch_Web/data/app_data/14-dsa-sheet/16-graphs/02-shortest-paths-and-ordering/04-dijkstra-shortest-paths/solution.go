package main

import (
	"container/heap"
	"fmt"
	"math"
)

type distItem struct{ d, v int }

type distHeap []distItem

func (h distHeap) Len() int           { return len(h) }
func (h distHeap) Less(i, j int) bool { return h[i].d < h[j].d }
func (h distHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *distHeap) Push(x any)        { *h = append(*h, x.(distItem)) }
func (h *distHeap) Pop() any {
	old := *h
	n := len(old)
	it := old[n-1]
	*h = old[:n-1]
	return it
}

// O((V + E) log V) time, O(V + E) space
func shortestDistances(n int, edges [][]int, source int) []int {
	const inf = math.MaxInt
	adj := make([][][2]int, n)
	for _, e := range edges {
		adj[e[0]] = append(adj[e[0]], [2]int{e[1], e[2]})
	}
	dist := make([]int, n)
	for i := range dist {
		dist[i] = inf
	}
	dist[source] = 0
	h := &distHeap{{0, source}}
	heap.Init(h)
	for h.Len() > 0 {
		it := heap.Pop(h).(distItem)
		if it.d > dist[it.v] {
			continue
		}
		for _, e := range adj[it.v] {
			v, w := e[0], e[1]
			if it.d+w < dist[v] {
				dist[v] = it.d + w
				heap.Push(h, distItem{dist[v], v})
			}
		}
	}
	for i := range dist {
		if dist[i] == inf {
			dist[i] = -1
		}
	}
	return dist
}

func main() {
	fmt.Println(shortestDistances(3, [][]int{[]int{0, 1, 4}, []int{0, 2, 1}, []int{2, 1, 2}}, 0))
}
