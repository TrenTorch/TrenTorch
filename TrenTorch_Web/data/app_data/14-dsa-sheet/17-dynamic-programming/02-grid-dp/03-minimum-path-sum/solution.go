package main

import "fmt"

// O(rows * cols) time, O(cols) space
func minPathSum(grid [][]int) int {
	rows := len(grid)
	cols := 0
	if rows > 0 {
		cols = len(grid[0])
	}
	if rows == 0 || cols == 0 {
		return 0
	}
	row := make([]int, cols)
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if r == 0 && c == 0 {
				row[c] = grid[0][0]
			} else if r == 0 {
				row[c] = row[c-1] + grid[r][c]
			} else if c == 0 {
				row[c] = row[c] + grid[r][c]
			} else {
				row[c] = min(row[c], row[c-1]) + grid[r][c]
			}
		}
	}
	return row[cols-1]
}

func main() {
	fmt.Println(minPathSum([][]int{[]int{1, 3, 1}, []int{1, 5, 1}, []int{4, 2, 1}}))
}
