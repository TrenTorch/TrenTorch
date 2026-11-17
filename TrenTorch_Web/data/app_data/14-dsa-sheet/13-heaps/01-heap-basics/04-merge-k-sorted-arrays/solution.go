package main

import (
	"container/heap"
	"fmt"
)

type mergeItem struct {
	value, row, col int
}

type mergeHeap []mergeItem

func (h mergeHeap) Len() int { return len(h) }
func (h mergeHeap) Less(i, j int) bool {
	a, b := h[i], h[j]
	if a.value != b.value {
		return a.value < b.value
	}
	if a.row != b.row {
		return a.row < b.row
	}
	return a.col < b.col
}
func (h mergeHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *mergeHeap) Push(x any)   { *h = append(*h, x.(mergeItem)) }
func (h *mergeHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

// O(N log k) time for N total values and k lists, O(k) heap space plus O(N) output
func mergeKArrays(arrays [][]int) []int {
	h := mergeHeap{}
	for i, arr := range arrays {
		if len(arr) > 0 {
			h = append(h, mergeItem{value: arr[0], row: i, col: 0})
		}
	}
	heap.Init(&h)
	out := make([]int, 0)
	for h.Len() > 0 {
		it := heap.Pop(&h).(mergeItem)
		out = append(out, it.value)
		if it.col+1 < len(arrays[it.row]) {
			heap.Push(&h, mergeItem{value: arrays[it.row][it.col+1], row: it.row, col: it.col + 1})
		}
	}
	return out
}

func main() {
	fmt.Println(mergeKArrays([][]int{[]int{1, 4, 5}, []int{1, 3, 4}, []int{2, 6}}))
}
