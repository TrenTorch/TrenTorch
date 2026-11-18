package main

import (
	"container/heap"
	"fmt"
)

type swimItem struct {
	t, x, y int
}

type swimHeap []swimItem

func (h swimHeap) Len() int { return len(h) }
func (h swimHeap) Less(i, j int) bool {
	if h[i].t != h[j].t {
		return h[i].t < h[j].t
	}
	if h[i].x != h[j].x {
		return h[i].x < h[j].x
	}
	return h[i].y < h[j].y
}
func (h swimHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *swimHeap) Push(x any)   { *h = append(*h, x.(swimItem)) }
func (h *swimHeap) Pop() any {
	old := *h
	n := len(old)
	item := old[n-1]
	*h = old[:n-1]
	return item
}

// O(n^2 log n) time, O(n^2) space
func swimInWater(grid [][]int) int {
	n, m := len(grid), len(grid[0])
	seen := make([][]bool, n)
	for i := range seen {
		seen[i] = make([]bool, m)
	}
	h := &swimHeap{{grid[0][0], 0, 0}}
	heap.Init(h)
	seen[0][0] = true
	dirs := [4][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}
	for h.Len() > 0 {
		item := heap.Pop(h).(swimItem)
		t, x, y := item.t, item.x, item.y
		if x == n-1 && y == m-1 {
			return t
		}
		for _, d := range dirs {
			nx, ny := x+d[0], y+d[1]
			if nx >= 0 && nx < n && ny >= 0 && ny < m && !seen[nx][ny] {
				seen[nx][ny] = true
				heap.Push(h, swimItem{max(t, grid[nx][ny]), nx, ny})
			}
		}
	}
	return 0
}

func main() {
	fmt.Println(swimInWater([][]int{[]int{0, 2}, []int{1, 3}}))
}
