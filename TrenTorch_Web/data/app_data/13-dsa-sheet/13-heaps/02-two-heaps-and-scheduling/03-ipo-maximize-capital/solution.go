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

type project struct {
	capital, profit int
}

// O(n log n + k log n) time, O(n) space
func findMaximizedCapital(k int, w int, profits []int, capital []int) int {
	projects := make([]project, len(capital))
	for i := range capital {
		projects[i] = project{capital: capital[i], profit: profits[i]}
	}
	sort.Slice(projects, func(i, j int) bool {
		if projects[i].capital != projects[j].capital {
			return projects[i].capital < projects[j].capital
		}
		return projects[i].profit < projects[j].profit
	})
	h := minIntHeap{}
	i := 0
	for step := 0; step < k; step++ {
		for i < len(projects) && projects[i].capital <= w {
			heap.Push(&h, -projects[i].profit)
			i++
		}
		if h.Len() == 0 {
			break
		}
		w += -(heap.Pop(&h).(int))
	}
	return w
}

func main() {
	fmt.Println(findMaximizedCapital(2, 0, []int{1, 2, 3}, []int{0, 1, 1}))
}
