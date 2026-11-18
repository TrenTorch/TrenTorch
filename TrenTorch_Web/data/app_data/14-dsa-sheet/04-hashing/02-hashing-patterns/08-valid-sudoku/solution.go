package main

import "fmt"

// O(1) time, O(1) space (fixed 9x9 board)
func validSudoku(board [][]int) bool {
	var rows, cols, boxes [9][10]bool
	for r := 0; r < 9; r++ {
		for c := 0; c < 9; c++ {
			digit := board[r][c]
			if digit == 0 {
				continue
			}
			b := (r/3)*3 + c/3
			if rows[r][digit] || cols[c][digit] || boxes[b][digit] {
				return false
			}
			rows[r][digit] = true
			cols[c][digit] = true
			boxes[b][digit] = true
		}
	}
	return true
}

func main() {
	fmt.Println(validSudoku([][]int{[]int{5, 3, 0, 0, 7, 0, 0, 0, 0}, []int{6, 0, 0, 1, 9, 5, 0, 0, 0}, []int{0, 9, 8, 0, 0, 0, 0, 6, 0}, []int{8, 0, 0, 0, 6, 0, 0, 0, 3}, []int{4, 0, 0, 8, 0, 3, 0, 0, 1}, []int{7, 0, 0, 0, 2, 0, 0, 0, 6}, []int{0, 6, 0, 0, 0, 0, 2, 8, 0}, []int{0, 0, 0, 4, 1, 9, 0, 0, 5}, []int{0, 0, 0, 0, 8, 0, 0, 7, 9}}))
}
