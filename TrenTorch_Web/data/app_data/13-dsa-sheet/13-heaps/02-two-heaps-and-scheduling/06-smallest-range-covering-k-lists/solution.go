package main

import (
	"container/heap"
	"fmt"
)

type rangeItem struct {
	value, row, col int
}

type rangeHeap []rangeItem

func (h rangeHeap) Len() int { return len(h) }
func (h rangeHeap) Less(i, j int) bool {
	a, b := h[i], h[j]
	if a.value != b.value {
		return a.value < b.value
	}
	if a.row != b.row {
		return a.row < b.row
	}
	return a.col < b.col
}
func (h rangeHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *rangeHeap) Push(x any)   { *h = append(*h, x.(rangeItem)) }
func (h *rangeHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

// O(N log k) time for N total values and k lists, O(k) space
func smallestRange(lists [][]int) []int {
	h := make(rangeHeap, 0, len(lists))
	currentMax := lists[0][0]
	for i, lst := range lists {
		h = append(h, rangeItem{value: lst[0], row: i, col: 0})
		if lst[0] > currentMax {
			currentMax = lst[0]
		}
	}
	heap.Init(&h)
	best := []int{h[0].value, currentMax}
	for {
		it := heap.Pop(&h).(rangeItem)
		value, i := it.value, it.row
		curDiff, bestDiff := currentMax-value, best[1]-best[0]
		if curDiff < bestDiff || (curDiff == bestDiff && value < best[0]) {
			best = []int{value, currentMax}
		}
		if it.col+1 == len(lists[i]) {
			return best
		}
		nxt := lists[i][it.col+1]
		currentMax = max(currentMax, nxt)
		heap.Push(&h, rangeItem{value: nxt, row: i, col: it.col + 1})
	}
}

func main() {
	fmt.Println(smallestRange([][]int{[]int{4, 10, 15, 24, 26}, []int{0, 9, 12, 20}, []int{5, 18, 22, 30}}))
}
