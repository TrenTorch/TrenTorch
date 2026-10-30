package main

import "fmt"

// O(r * c) time, O(r * c) space for the new matrix.
func transposeMatrix(matrix [][]int) [][]int {
	if len(matrix) == 0 || len(matrix[0]) == 0 {
		return [][]int{}
	}
	rows, cols := len(matrix), len(matrix[0])
	out := make([][]int, cols)
	for j := range out {
		out[j] = make([]int, rows)
		for i := 0; i < rows; i++ {
			out[j][i] = matrix[i][j]
		}
	}
	return out
}

func main() {
	fmt.Println(transposeMatrix([][]int{[]int{1, 2, 3}, []int{4, 5, 6}}))
}
