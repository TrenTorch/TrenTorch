package main

import "fmt"

// O(log(rows * cols)) time, O(1) space
func searchMatrix(matrix [][]int, target int) bool {
	if len(matrix) == 0 || len(matrix[0]) == 0 {
		return false
	}
	rows, cols := len(matrix), len(matrix[0])
	lo, hi := 0, rows*cols-1
	for lo <= hi {
		mid := (lo + hi) / 2
		value := matrix[mid/cols][mid%cols]
		if value == target {
			return true
		}
		if value < target {
			lo = mid + 1
		} else {
			hi = mid - 1
		}
	}
	return false
}

func main() {
	fmt.Println(searchMatrix([][]int{[]int{1, 3, 5, 7}, []int{10, 11, 16, 20}, []int{23, 30, 34, 60}}, 3))
}
