package main

import (
	"container/heap"
	"fmt"
)

type intHeap []int

func (h intHeap) Len() int           { return len(h) }
func (h intHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h intHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *intHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *intHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

// O((V + E) log V) time, O(V + E) space
func findOrder(numCourses int, prerequisites [][]int) []int {
	adj := make([][]int, numCourses)
	inDegree := make([]int, numCourses)
	for _, p := range prerequisites {
		course, pre := p[0], p[1]
		adj[pre] = append(adj[pre], course)
		inDegree[course]++
	}
	h := &intHeap{}
	for v := 0; v < numCourses; v++ {
		if inDegree[v] == 0 {
			*h = append(*h, v)
		}
	}
	heap.Init(h)
	order := []int{}
	for h.Len() > 0 {
		node := heap.Pop(h).(int)
		order = append(order, node)
		for _, nxt := range adj[node] {
			inDegree[nxt]--
			if inDegree[nxt] == 0 {
				heap.Push(h, nxt)
			}
		}
	}
	if len(order) != numCourses {
		return []int{}
	}
	return order
}

func main() {
	fmt.Println(findOrder(4, [][]int{[]int{1, 0}, []int{2, 0}, []int{3, 1}, []int{3, 2}}))
}
