package main

import "fmt"

// O(rows * cols) time, O(cols) space
func uniquePathsObstacles(grid [][]int) int {
	const mod = 1000000007
	rows := len(grid)
	cols := 0
	if rows > 0 {
		cols = len(grid[0])
	}
	if rows == 0 || cols == 0 {
		return 0
	}
	row := make([]int, cols)
	if grid[0][0] == 0 {
		row[0] = 1
	}
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if grid[r][c] == 1 {
				row[c] = 0
			} else if c > 0 {
				row[c] = (row[c] + row[c-1]) % mod
			}
		}
	}
	return row[cols-1]
}

func main() {
	fmt.Println(uniquePathsObstacles([][]int{[]int{0, 0, 0}, []int{0, 1, 0}, []int{0, 0, 0}}))
}
