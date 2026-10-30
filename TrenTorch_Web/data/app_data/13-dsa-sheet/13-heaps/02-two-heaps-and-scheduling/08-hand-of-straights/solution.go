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
func isNStraightHand(hand []int, groupSize int) bool {
	if len(hand)%groupSize != 0 {
		return false
	}
	count := map[int]int{}
	for _, x := range hand {
		count[x]++
	}
	h := make(minIntHeap, 0, len(count))
	for x := range count {
		h = append(h, x)
	}
	heap.Init(&h)
	for h.Len() > 0 {
		start := h[0]
		for x := start; x < start+groupSize; x++ {
			if count[x] == 0 {
				return false
			}
			count[x]--
			if count[x] == 0 {
				if x != h[0] {
					return false
				}
				heap.Pop(&h)
			}
		}
	}
	return true
}

func main() {
	fmt.Println(isNStraightHand([]int{1, 2, 3, 6, 2, 3, 4, 7, 8}, 3))
}
