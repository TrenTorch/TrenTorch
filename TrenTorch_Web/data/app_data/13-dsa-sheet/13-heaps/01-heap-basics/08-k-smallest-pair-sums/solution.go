package main

import (
	"container/heap"
	"fmt"
)

type pairItem struct {
	total, i, j int
}

type pairHeap []pairItem

func (h pairHeap) Len() int { return len(h) }
func (h pairHeap) Less(a, b int) bool {
	x, y := h[a], h[b]
	if x.total != y.total {
		return x.total < y.total
	}
	if x.i != y.i {
		return x.i < y.i
	}
	return x.j < y.j
}
func (h pairHeap) Swap(a, b int) { h[a], h[b] = h[b], h[a] }
func (h *pairHeap) Push(x any)   { *h = append(*h, x.(pairItem)) }
func (h *pairHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

// O(k log min(n, k)) time, O(min(n, k)) space
func kSmallestPairSums(nums1 []int, nums2 []int, k int) []int {
	out := []int{}
	if len(nums1) == 0 || len(nums2) == 0 || k <= 0 {
		return out
	}
	initial := min(len(nums1), k)
	h := make(pairHeap, 0, initial)
	for i := 0; i < initial; i++ {
		h = append(h, pairItem{total: nums1[i] + nums2[0], i: i, j: 0})
	}
	heap.Init(&h)
	for h.Len() > 0 && len(out) < k {
		it := heap.Pop(&h).(pairItem)
		out = append(out, it.total)
		if it.j+1 < len(nums2) {
			heap.Push(&h, pairItem{total: nums1[it.i] + nums2[it.j+1], i: it.i, j: it.j + 1})
		}
	}
	return out
}

func main() {
	fmt.Println(kSmallestPairSums([]int{1, 7, 11}, []int{2, 4, 6}, 3))
}
