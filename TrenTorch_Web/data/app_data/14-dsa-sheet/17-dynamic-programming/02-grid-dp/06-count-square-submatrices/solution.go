package main

import "fmt"

// O(rows * cols) time, O(cols) space
func countSquares(matrix [][]int) int {
	rows := len(matrix)
	cols := 0
	if rows > 0 {
		cols = len(matrix[0])
	}
	prev := make([]int, cols+1)
	total := 0
	for r := 0; r < rows; r++ {
		cur := make([]int, cols+1)
		for c := 0; c < cols; c++ {
			if matrix[r][c] == 1 {
				cur[c+1] = 1 + min(prev[c], prev[c+1], cur[c])
				total += cur[c+1]
			}
		}
		prev = cur
	}
	return total
}

func main() {
	fmt.Println(countSquares([][]int{[]int{0, 1, 1, 1}, []int{1, 1, 1, 1}, []int{0, 1, 1, 1}}))
}
