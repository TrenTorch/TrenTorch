package main

import "fmt"

// O((rows + cols) * log(max(rows, cols))) time, O(log(max(rows, cols))) space
func searchMatrixIi(matrix [][]int, target int) bool {
	if len(matrix) == 0 || len(matrix[0]) == 0 {
		return false
	}

	var search func(r0, r1, c0, c1 int) bool
	search = func(r0, r1, c0, c1 int) bool {
		// looks for target in rows r0..r1 and columns c0..c1 (both inclusive)
		if r0 > r1 || c0 > c1 {
			return false
		}
		if r1-r0 <= c1-c0 {
			r := (r0 + r1) / 2
			lo, hi := c0, c1+1
			for lo < hi {
				mid := (lo + hi) / 2
				if matrix[r][mid] < target {
					lo = mid + 1
				} else {
					hi = mid
				}
			}
			if lo <= c1 && matrix[r][lo] == target {
				return true
			}
			return search(r0, r-1, lo, c1) || search(r+1, r1, c0, lo-1)
		}
		c := (c0 + c1) / 2
		lo, hi := r0, r1+1
		for lo < hi {
			mid := (lo + hi) / 2
			if matrix[mid][c] < target {
				lo = mid + 1
			} else {
				hi = mid
			}
		}
		if lo <= r1 && matrix[lo][c] == target {
			return true
		}
		return search(r0, lo-1, c+1, c1) || search(lo, r1, c0, c-1)
	}

	return search(0, len(matrix)-1, 0, len(matrix[0])-1)
}

func main() {
	fmt.Println(searchMatrixIi([][]int{[]int{1, 4, 7, 11}, []int{2, 5, 8, 12}, []int{3, 6, 9, 16}, []int{10, 13, 14, 17}}, 5))
}
