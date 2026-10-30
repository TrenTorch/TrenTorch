package main

import (
	"container/heap"
	"fmt"
)

type maxHeap []int

func (h maxHeap) Len() int           { return len(h) }
func (h maxHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h maxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *maxHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *maxHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

// O(n log n) time, O(n) space
func lastStoneWeight(stones []int) int {
	h := make(maxHeap, len(stones))
	copy(h, stones)
	heap.Init(&h)
	for h.Len() > 1 {
		a := heap.Pop(&h).(int)
		b := heap.Pop(&h).(int)
		if a != b {
			heap.Push(&h, a-b)
		}
	}
	if h.Len() == 0 {
		return 0
	}
	return h[0]
}

func main() {
	fmt.Println(lastStoneWeight([]int{2, 7, 4, 1, 8, 1}))
}
