package main

import "fmt"

// O((rows + cols) * log(max - min)) time, O(1) space
func kthSmallestMatrix(matrix [][]int, k int) int {
	rows, cols := len(matrix), len(matrix[0])

	countAtMost := func(x int) int {
		count := 0
		col := cols - 1
		for r := 0; r < rows; r++ {
			for col >= 0 && matrix[r][col] > x {
				col--
			}
			count += col + 1
		}
		return count
	}

	lo, hi := matrix[0][0], matrix[rows-1][cols-1]
	for lo < hi {
		mid := lo + (hi-lo)/2
		if countAtMost(mid) >= k {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func main() {
	fmt.Println(kthSmallestMatrix([][]int{[]int{1, 5, 9}, []int{10, 11, 13}, []int{12, 13, 15}}, 8))
}
