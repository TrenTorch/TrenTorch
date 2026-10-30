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

// O(n log k) time, O(k) space
func sortKSorted(nums []int, k int) []int {
	end := min(k+1, len(nums))
	h := make(minIntHeap, end)
	copy(h, nums[:end])
	heap.Init(&h)
	out := make([]int, 0, len(nums))
	for _, x := range nums[end:] {
		out = append(out, pushPop(&h, x))
	}
	for h.Len() > 0 {
		out = append(out, heap.Pop(&h).(int))
	}
	return out
}

func main() {
	fmt.Println(sortKSorted([]int{6, 5, 3, 2, 8, 10, 9}, 3))
}
