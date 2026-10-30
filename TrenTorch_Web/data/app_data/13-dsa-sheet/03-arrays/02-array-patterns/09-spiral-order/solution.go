package main

import "fmt"

// O(m * n) time, O(m * n) space for the output
func spiralOrder(matrix [][]int) []int {
	if len(matrix) == 0 || len(matrix[0]) == 0 {
		return []int{}
	}
	out := []int{}
	top, bottom := 0, len(matrix)-1
	left, right := 0, len(matrix[0])-1
	for top <= bottom && left <= right {
		for c := left; c <= right; c++ {
			out = append(out, matrix[top][c])
		}
		for i := top + 1; i <= bottom; i++ {
			out = append(out, matrix[i][right])
		}
		if top < bottom {
			for c := right - 1; c >= left; c-- {
				out = append(out, matrix[bottom][c])
			}
		}
		if left < right {
			for i := bottom - 1; i > top; i-- {
				out = append(out, matrix[i][left])
			}
		}
		top++
		bottom--
		left++
		right--
	}
	return out
}

func main() {
	fmt.Println(spiralOrder([][]int{[]int{1, 2, 3}, []int{4, 5, 6}, []int{7, 8, 9}}))
}
