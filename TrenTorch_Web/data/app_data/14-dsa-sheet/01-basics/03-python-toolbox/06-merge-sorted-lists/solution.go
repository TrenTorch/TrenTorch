package main

import (
	"container/heap"
	"fmt"
)

// item is the current head value of one input list.
type item struct {
	val  int
	list int
	idx  int
}

// minHeap orders items by value.
type minHeap []item

func (h minHeap) Len() int           { return len(h) }
func (h minHeap) Less(i, j int) bool { return h[i].val < h[j].val }
func (h minHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *minHeap) Push(x any) {
	*h = append(*h, x.(item))
}

func (h *minHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

// O(N log k) time, O(k) heap space plus O(N) output, where N is the total
// number of values and k is the number of lists
func mergeSortedLists(lists [][]int) []int {
	total := 0
	h := &minHeap{}
	for i, l := range lists {
		total += len(l)
		if len(l) > 0 {
			*h = append(*h, item{l[0], i, 0})
		}
	}
	heap.Init(h)
	out := make([]int, 0, total)
	for h.Len() > 0 {
		it := heap.Pop(h).(item)
		out = append(out, it.val)
		if next := it.idx + 1; next < len(lists[it.list]) {
			heap.Push(h, item{lists[it.list][next], it.list, next})
		}
	}
	return out
}

func main() {
	fmt.Println(mergeSortedLists([][]int{[]int{1, 4, 7}, []int{2, 5}, []int{3, 6, 9}}))
}
