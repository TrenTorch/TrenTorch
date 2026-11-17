package main

import (
	"container/heap"
	"fmt"
)

type intHeap []int

func (h intHeap) Len() int           { return len(h) }
func (h intHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h intHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *intHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *intHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

// O(C + N * L + E log C) time, O(C + E) space (C = distinct letters, E = order pairs)
func alienOrder(words []string) string {
	var present [256]bool
	for _, w := range words {
		for i := 0; i < len(w); i++ {
			present[w[i]] = true
		}
	}
	type pair struct{ x, y byte }
	edges := map[pair]bool{}
	for k := 0; k+1 < len(words); k++ {
		a, b := words[k], words[k+1]
		found := false
		for i := 0; i < len(a) && i < len(b); i++ {
			if a[i] != b[i] {
				edges[pair{a[i], b[i]}] = true
				found = true
				break
			}
		}
		if !found && len(a) > len(b) {
			return ""
		}
	}
	var adj [256][]int
	var inDegree [256]int
	for e := range edges {
		adj[e.x] = append(adj[e.x], int(e.y))
		inDegree[e.y]++
	}
	h := &intHeap{}
	total := 0
	for c := 0; c < 256; c++ {
		if present[c] {
			total++
			if inDegree[c] == 0 {
				*h = append(*h, c)
			}
		}
	}
	heap.Init(h)
	out := []byte{}
	for h.Len() > 0 {
		c := heap.Pop(h).(int)
		out = append(out, byte(c))
		for _, nxt := range adj[c] {
			inDegree[nxt]--
			if inDegree[nxt] == 0 {
				heap.Push(h, nxt)
			}
		}
	}
	if len(out) != total {
		return ""
	}
	return string(out)
}

func main() {
	fmt.Println(alienOrder([]string{"wrt", "wrf", "er", "ett", "rftt"}))
}
