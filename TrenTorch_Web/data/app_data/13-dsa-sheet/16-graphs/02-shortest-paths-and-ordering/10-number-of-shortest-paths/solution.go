package main

import (
	"container/heap"
	"fmt"
)

type distItem struct {
	d, u int
}

type distHeap []distItem

func (h distHeap) Len() int { return len(h) }
func (h distHeap) Less(i, j int) bool {
	if h[i].d != h[j].d {
		return h[i].d < h[j].d
	}
	return h[i].u < h[j].u
}
func (h distHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *distHeap) Push(x any)   { *h = append(*h, x.(distItem)) }
func (h *distHeap) Pop() any {
	old := *h
	n := len(old)
	item := old[n-1]
	*h = old[:n-1]
	return item
}

type road struct {
	to, t int
}

// O(E log V) time, O(V + E) space
func countShortestPaths(n int, roads [][]int) int {
	const mod = 1000000007
	const inf = int(^uint(0) >> 1)
	adj := make([][]road, n)
	for _, r := range roads {
		a, b, t := r[0], r[1], r[2]
		adj[a] = append(adj[a], road{b, t})
		adj[b] = append(adj[b], road{a, t})
	}
	dist := make([]int, n)
	ways := make([]int, n)
	for i := range dist {
		dist[i] = inf
	}
	dist[0] = 0
	ways[0] = 1
	h := &distHeap{{0, 0}}
	heap.Init(h)
	for h.Len() > 0 {
		item := heap.Pop(h).(distItem)
		d, u := item.d, item.u
		if d > dist[u] {
			continue
		}
		for _, e := range adj[u] {
			v, t := e.to, e.t
			nd := d + t
			if nd < dist[v] {
				dist[v] = nd
				ways[v] = ways[u]
				heap.Push(h, distItem{nd, v})
			} else if nd == dist[v] {
				ways[v] = (ways[v] + ways[u]) % mod
			}
		}
	}
	return ways[n-1] % mod
}

func main() {
	fmt.Println(countShortestPaths(4, [][]int{[]int{0, 1, 1}, []int{0, 2, 1}, []int{1, 3, 1}, []int{2, 3, 1}}))
}
