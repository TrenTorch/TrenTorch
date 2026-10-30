package main

import "fmt"

// O(9^m) worst-case time for m empty cells (pruned by candidate sets), O(81) extra space
func sudokuSolver(board [][]int) [][]int {
	grid := make([][]int, 9)
	for r := 0; r < 9; r++ {
		grid[r] = append([]int(nil), board[r]...)
	}
	var rows, cols, boxes [9][10]bool
	type cell struct{ r, c int }
	var empty []cell
	for r := 0; r < 9; r++ {
		for c := 0; c < 9; c++ {
			v := grid[r][c]
			if v != 0 {
				rows[r][v] = true
				cols[c][v] = true
				boxes[r/3*3+c/3][v] = true
			} else {
				empty = append(empty, cell{r, c})
			}
		}
	}
	candidates := func(r, c int) []int {
		var opts []int
		for v := 1; v <= 9; v++ {
			if !rows[r][v] && !cols[c][v] && !boxes[r/3*3+c/3][v] {
				opts = append(opts, v)
			}
		}
		return opts
	}
	var rec func() bool
	rec = func() bool {
		found := false
		var bestR, bestC int
		var bestOpts []int
		for _, e := range empty {
			if grid[e.r][e.c] != 0 {
				continue
			}
			opts := candidates(e.r, e.c)
			if !found || len(opts) < len(bestOpts) {
				found = true
				bestR, bestC, bestOpts = e.r, e.c, opts
				if len(opts) <= 1 {
					break
				}
			}
		}
		if !found {
			return true
		}
		r, c := bestR, bestC
		for _, v := range bestOpts {
			grid[r][c] = v
			rows[r][v], cols[c][v], boxes[r/3*3+c/3][v] = true, true, true
			if rec() {
				return true
			}
			grid[r][c] = 0
			rows[r][v], cols[c][v], boxes[r/3*3+c/3][v] = false, false, false
		}
		return false
	}
	rec()
	return grid
}

func main() {
	fmt.Println(sudokuSolver([][]int{[]int{5, 3, 0, 0, 7, 0, 0, 0, 0}, []int{6, 0, 0, 1, 9, 5, 0, 0, 0}, []int{0, 9, 8, 0, 0, 0, 0, 6, 0}, []int{8, 0, 0, 0, 6, 0, 0, 0, 3}, []int{4, 0, 0, 8, 0, 3, 0, 0, 1}, []int{7, 0, 0, 0, 2, 0, 0, 0, 6}, []int{0, 6, 0, 0, 0, 0, 2, 8, 0}, []int{0, 0, 0, 4, 1, 9, 0, 0, 5}, []int{0, 0, 0, 0, 8, 0, 0, 7, 9}}))
}
