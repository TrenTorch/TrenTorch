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
func runningMedian(nums []int) []float64 {
	low := minIntHeap{}  // stores negated values: max-heap of the lower half
	high := minIntHeap{} // min-heap of the upper half
	out := make([]float64, 0, len(nums))
	for _, x := range nums {
		heap.Push(&low, -x)
		top := heap.Pop(&low).(int)
		heap.Push(&high, -top)
		if high.Len() > low.Len() {
			heap.Push(&low, -(heap.Pop(&high).(int)))
		}
		if low.Len() > high.Len() {
			out = append(out, float64(-low[0]))
		} else {
			out = append(out, float64(-low[0]+high[0])/2)
		}
	}
	return out
}

func main() {
	fmt.Println(runningMedian([]int{5, 15, 1, 3}))
}
