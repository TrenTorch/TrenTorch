package main

import "fmt"

// O(m * n) time, O(m * n) space
func rotateMatrix(matrix [][]int) [][]int {
	m := len(matrix)
	if m == 0 {
		return [][]int{}
	}
	n := len(matrix[0])
	result := make([][]int, n)
	for r := 0; r < n; r++ {
		result[r] = make([]int, m)
		for c := 0; c < m; c++ {
			result[r][c] = matrix[m-1-c][r]
		}
	}
	return result
}

func main() {
	fmt.Println(rotateMatrix([][]int{[]int{1, 2, 3}, []int{4, 5, 6}}))
}
