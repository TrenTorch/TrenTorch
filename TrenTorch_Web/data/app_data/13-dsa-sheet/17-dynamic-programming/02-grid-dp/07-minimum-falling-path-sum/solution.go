package main

import "fmt"

// O(rows * cols) time, O(cols) space
func minFallingPathSum(matrix [][]int) int {
	if len(matrix) == 0 || len(matrix[0]) == 0 {
		return 0
	}
	prev := make([]int, len(matrix[0]))
	copy(prev, matrix[0])
	cols := len(prev)
	for r := 1; r < len(matrix); r++ {
		next := make([]int, cols)
		for c := 0; c < cols; c++ {
			lo := c - 1
			if lo < 0 {
				lo = 0
			}
			hi := c + 2
			if hi > cols {
				hi = cols
			}
			m := prev[lo]
			for k := lo + 1; k < hi; k++ {
				m = min(m, prev[k])
			}
			next[c] = matrix[r][c] + m
		}
		prev = next
	}
	m := prev[0]
	for _, v := range prev[1:] {
		m = min(m, v)
	}
	return m
}

func main() {
	fmt.Println(minFallingPathSum([][]int{[]int{2, 1, 3}, []int{6, 5, 4}, []int{7, 8, 9}}))
}
