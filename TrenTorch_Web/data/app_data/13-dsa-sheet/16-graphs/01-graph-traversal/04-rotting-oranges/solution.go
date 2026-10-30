package main

import "fmt"

type cell struct{ r, c int }

// O(R*C) time, O(R*C) space
func orangesRotting(grid [][]int) int {
	rows := len(grid)
	cols := 0
	if rows > 0 {
		cols = len(grid[0])
	}
	g := make([][]int, rows)
	for r := range g {
		g[r] = make([]int, cols)
		copy(g[r], grid[r])
	}
	queue := []cell{}
	fresh := 0
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if g[r][c] == 2 {
				queue = append(queue, cell{r, c})
			} else if g[r][c] == 1 {
				fresh++
			}
		}
	}
	minutes := 0
	head := 0
	for head < len(queue) && fresh > 0 {
		minutes++
		levelEnd := len(queue)
		for ; head < levelEnd; head++ {
			cur := queue[head]
			for _, d := range [4]cell{{cur.r + 1, cur.c}, {cur.r - 1, cur.c}, {cur.r, cur.c + 1}, {cur.r, cur.c - 1}} {
				if d.r >= 0 && d.r < rows && d.c >= 0 && d.c < cols && g[d.r][d.c] == 1 {
					g[d.r][d.c] = 2
					fresh--
					queue = append(queue, d)
				}
			}
		}
	}
	if fresh == 0 {
		return minutes
	}
	return -1
}

func main() {
	fmt.Println(orangesRotting([][]int{[]int{2, 1, 1}, []int{1, 1, 0}, []int{0, 1, 1}}))
}
