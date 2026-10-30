package main

import (
	"container/heap"
	"fmt"
	"sort"
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
func minMeetingRooms(meetings [][]int) int {
	sorted := make([][]int, len(meetings))
	copy(sorted, meetings)
	sort.Slice(sorted, func(i, j int) bool {
		if sorted[i][0] != sorted[j][0] {
			return sorted[i][0] < sorted[j][0]
		}
		return sorted[i][1] < sorted[j][1]
	})
	rooms := minIntHeap{}
	for _, m := range sorted {
		start, end := m[0], m[1]
		if rooms.Len() > 0 && rooms[0] <= start {
			rooms[0] = end
			heap.Fix(&rooms, 0)
		} else {
			heap.Push(&rooms, end)
		}
	}
	return rooms.Len()
}

func main() {
	fmt.Println(minMeetingRooms([][]int{[]int{0, 30}, []int{5, 10}, []int{15, 20}}))
}
