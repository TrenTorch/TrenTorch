package main

import "fmt"

// O(n^2) time, O(n) space where n is the number of rows
func minimumTotal(triangle [][]int) int {
	if len(triangle) == 0 {
		return 0
	}
	last := triangle[len(triangle)-1]
	best := make([]int, len(last))
	copy(best, last)
	for row := len(triangle) - 2; row >= 0; row-- {
		for j := 0; j <= row; j++ {
			best[j] = triangle[row][j] + min(best[j], best[j+1])
		}
	}
	return best[0]
}

func main() {
	fmt.Println(minimumTotal([][]int{[]int{2}, []int{3, 4}, []int{6, 5, 7}, []int{4, 1, 8, 3}}))
}
