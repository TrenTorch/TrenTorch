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

// O(n log l) time where l = ladders in use at once, O(n) space
func furthestBuilding(heights []int, bricks int, ladders int) int {
	h := minIntHeap{}
	for i := 1; i < len(heights); i++ {
		climb := heights[i] - heights[i-1]
		if climb <= 0 {
			continue
		}
		heap.Push(&h, climb)
		if h.Len() > ladders {
			bricks -= heap.Pop(&h).(int)
			if bricks < 0 {
				return i - 1
			}
		}
	}
	return len(heights) - 1
}

func main() {
	fmt.Println(furthestBuilding([]int{4, 2, 7, 6, 9, 14, 12}, 5, 1))
}
