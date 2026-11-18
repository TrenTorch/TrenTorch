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

// pushPop mirrors heapq.heappushpop: push x, then pop the smallest value.
func pushPop(h *minIntHeap, x int) int {
	if h.Len() > 0 && (*h)[0] < x {
		top := (*h)[0]
		(*h)[0] = x
		heap.Fix(h, 0)
		return top
	}
	return x
}

// O((len(nums) + len(adds)) log k) time, O(k) space
func kthLargestStream(k int, nums []int, adds []int) []int {
	h := minIntHeap{}
	for _, x := range nums {
		heap.Push(&h, x)
		if h.Len() > k {
			heap.Pop(&h)
		}
	}
	out := make([]int, 0, len(adds))
	for _, x := range adds {
		if h.Len() < k {
			heap.Push(&h, x)
		} else {
			pushPop(&h, x)
		}
		out = append(out, h[0])
	}
	return out
}

func main() {
	fmt.Println(kthLargestStream(3, []int{4, 5, 8, 2}, []int{3, 5, 10, 9, 4}))
}
