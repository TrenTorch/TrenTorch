package main

import "fmt"

// O(R*C) time, O(R*C) space
func largestIsland(grid [][]int) int {
	rows := len(grid)
	cols := 0
	if rows > 0 {
		cols = len(grid[0])
	}
	dirs := [4][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}
	label := make([][]int, rows)
	for i := range label {
		label[i] = make([]int, cols)
	}
	// size[id] is the island size for label id; index 0 means "no island".
	size := []int{0}
	nextID := 1
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if grid[r][c] == 1 && label[r][c] == 0 {
				label[r][c] = nextID
				stack := [][2]int{{r, c}}
				count := 0
				for len(stack) > 0 {
					top := stack[len(stack)-1]
					stack = stack[:len(stack)-1]
					x, y := top[0], top[1]
					count++
					for _, d := range dirs {
						nx, ny := x+d[0], y+d[1]
						if nx >= 0 && nx < rows && ny >= 0 && ny < cols && grid[nx][ny] == 1 && label[nx][ny] == 0 {
							label[nx][ny] = nextID
							stack = append(stack, [2]int{nx, ny})
						}
					}
				}
				size = append(size, count)
				nextID++
			}
		}
	}
	best := 0
	for _, s := range size {
		best = max(best, s)
	}
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if grid[r][c] == 0 {
				seen := map[int]bool{}
				total := 1
				for _, d := range dirs {
					nx, ny := r+d[0], c+d[1]
					if nx >= 0 && nx < rows && ny >= 0 && ny < cols && label[nx][ny] != 0 {
						id := label[nx][ny]
						if !seen[id] {
							seen[id] = true
							total += size[id]
						}
					}
				}
				best = max(best, total)
			}
		}
	}
	return best
}

func main() {
	fmt.Println(largestIsland([][]int{[]int{1, 0}, []int{0, 1}}))
}
