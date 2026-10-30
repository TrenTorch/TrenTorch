package main

import (
	"container/heap"
	"fmt"
)

type effortItem struct {
	e, x, y int
}

type effortHeap []effortItem

func (h effortHeap) Len() int { return len(h) }
func (h effortHeap) Less(i, j int) bool {
	if h[i].e != h[j].e {
		return h[i].e < h[j].e
	}
	if h[i].x != h[j].x {
		return h[i].x < h[j].x
	}
	return h[i].y < h[j].y
}
func (h effortHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *effortHeap) Push(x any)   { *h = append(*h, x.(effortItem)) }
func (h *effortHeap) Pop() any {
	old := *h
	n := len(old)
	item := old[n-1]
	*h = old[:n-1]
	return item
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

// O(R*C log(R*C)) time, O(R*C) space
func minimumEffortPath(heights [][]int) int {
	rows, cols := len(heights), len(heights[0])
	const inf = int(^uint(0) >> 1)
	effort := make([][]int, rows)
	for i := range effort {
		effort[i] = make([]int, cols)
		for j := range effort[i] {
			effort[i][j] = inf
		}
	}
	effort[0][0] = 0
	h := &effortHeap{{0, 0, 0}}
	heap.Init(h)
	dirs := [4][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}
	for h.Len() > 0 {
		item := heap.Pop(h).(effortItem)
		e, x, y := item.e, item.x, item.y
		if x == rows-1 && y == cols-1 {
			return e
		}
		if e > effort[x][y] {
			continue
		}
		for _, d := range dirs {
			nx, ny := x+d[0], y+d[1]
			if nx >= 0 && nx < rows && ny >= 0 && ny < cols {
				ne := max(e, abs(heights[nx][ny]-heights[x][y]))
				if ne < effort[nx][ny] {
					effort[nx][ny] = ne
					heap.Push(h, effortItem{ne, nx, ny})
				}
			}
		}
	}
	return 0
}

func main() {
	fmt.Println(minimumEffortPath([][]int{[]int{1, 2, 2}, []int{3, 8, 2}, []int{5, 3, 5}}))
}
