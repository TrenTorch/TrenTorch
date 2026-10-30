package main

import "fmt"

type cell struct{ r, c int }

// O(R*C) time, O(R*C) space
func maxIslandArea(grid [][]int) int {
	rows := len(grid)
	cols := 0
	if rows > 0 {
		cols = len(grid[0])
	}
	seen := make([][]bool, rows)
	for i := range seen {
		seen[i] = make([]bool, cols)
	}
	best := 0
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if grid[r][c] == 1 && !seen[r][c] {
				seen[r][c] = true
				stack := []cell{{r, c}}
				size := 0
				for len(stack) > 0 {
					cur := stack[len(stack)-1]
					stack = stack[:len(stack)-1]
					size++
					for _, d := range [4]cell{{cur.r + 1, cur.c}, {cur.r - 1, cur.c}, {cur.r, cur.c + 1}, {cur.r, cur.c - 1}} {
						if d.r >= 0 && d.r < rows && d.c >= 0 && d.c < cols && grid[d.r][d.c] == 1 && !seen[d.r][d.c] {
							seen[d.r][d.c] = true
							stack = append(stack, d)
						}
					}
				}
				if size > best {
					best = size
				}
			}
		}
	}
	return best
}

func main() {
	fmt.Println(maxIslandArea([][]int{[]int{1, 1, 0}, []int{0, 1, 0}, []int{0, 0, 1}}))
}
