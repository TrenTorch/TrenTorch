package main

import "fmt"

// O(rows + cols) time, O(1) space
func rowWithMostOnes(matrix [][]int) int {
	bestRow := -1
	col := 0
	if len(matrix) > 0 {
		col = len(matrix[0])
	}
	for i, row := range matrix {
		moved := false
		for col > 0 && row[col-1] == 1 {
			col--
			moved = true
		}
		if moved {
			bestRow = i
		}
	}
	return bestRow
}

func main() {
	fmt.Println(rowWithMostOnes([][]int{[]int{0, 0, 1, 1}, []int{0, 1, 1, 1}, []int{0, 0, 0, 1}}))
}
