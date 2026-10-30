package main

import (
	"container/heap"
	"fmt"
)

type minIntHeap []int

func (h minIntHeap) Len() int           { return len(h) }
func (h minIntHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h minIntHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *minIntHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *minIntHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

// O(n log n) time, O(n) space
func connectRopes(ropes []int) int {
	h := make(minIntHeap, len(ropes))
	copy(h, ropes)
	heap.Init(&h)
	total := 0
	for h.Len() > 1 {
		a := heap.Pop(&h).(int)
		b := heap.Pop(&h).(int)
		joined := a + b
		total += joined
		heap.Push(&h, joined)
	}
	return total
}

func main() {
	fmt.Println(connectRopes([]int{4, 3, 2, 6}))
}
