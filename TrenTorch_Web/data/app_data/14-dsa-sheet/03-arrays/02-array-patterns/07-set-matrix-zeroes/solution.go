package main

import "fmt"

// O(m * n) time, O(m + n) space
func setMatrixZeroes(matrix [][]int) [][]int {
	zeroRows := map[int]bool{}
	zeroCols := map[int]bool{}
	for i, row := range matrix {
		for j, x := range row {
			if x == 0 {
				zeroRows[i] = true
				zeroCols[j] = true
			}
		}
	}
	result := make([][]int, len(matrix))
	for i, row := range matrix {
		result[i] = make([]int, len(row))
		for j, x := range row {
			if zeroRows[i] || zeroCols[j] {
				result[i][j] = 0
			} else {
				result[i][j] = x
			}
		}
	}
	return result
}

func main() {
	fmt.Println(setMatrixZeroes([][]int{[]int{1, 2, 3}, []int{4, 0, 6}, []int{7, 8, 9}}))
}
