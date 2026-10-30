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
func minRefuelStops(target int, startFuel int, stations [][]int) int {
	h := minIntHeap{} // stores negated fuel amounts
	reach := startFuel
	stops := 0
	i := 0
	for reach < target {
		for i < len(stations) && stations[i][0] <= reach {
			heap.Push(&h, -stations[i][1])
			i++
		}
		if h.Len() == 0 {
			return -1
		}
		reach += -(heap.Pop(&h).(int))
		stops++
	}
	return stops
}

func main() {
	fmt.Println(minRefuelStops(100, 10, [][]int{[]int{10, 60}, []int{20, 30}, []int{30, 30}, []int{60, 40}}))
}
