package main

import "fmt"

type cell struct{ r, c int }

// O(R*C) time, O(R*C) space
func pacificAtlantic(heights [][]int) [][]int {
	rows := len(heights)
	cols := 0
	if rows > 0 {
		cols = len(heights[0])
	}
	result := [][]int{}
	if rows == 0 || cols == 0 {
		return result
	}

	flood := func(starts []cell) [][]bool {
		seen := make([][]bool, rows)
		for i := range seen {
			seen[i] = make([]bool, cols)
		}
		stack := make([]cell, 0, len(starts))
		for _, s := range starts {
			if !seen[s.r][s.c] {
				seen[s.r][s.c] = true
				stack = append(stack, s)
			}
		}
		for len(stack) > 0 {
			cur := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			for _, d := range [4]cell{{cur.r + 1, cur.c}, {cur.r - 1, cur.c}, {cur.r, cur.c + 1}, {cur.r, cur.c - 1}} {
				if d.r >= 0 && d.r < rows && d.c >= 0 && d.c < cols && !seen[d.r][d.c] && heights[d.r][d.c] >= heights[cur.r][cur.c] {
					seen[d.r][d.c] = true
					stack = append(stack, d)
				}
			}
		}
		return seen
	}

	var pacStarts, atlStarts []cell
	for r := 0; r < rows; r++ {
		pacStarts = append(pacStarts, cell{r, 0})
		atlStarts = append(atlStarts, cell{r, cols - 1})
	}
	for c := 0; c < cols; c++ {
		pacStarts = append(pacStarts, cell{0, c})
		atlStarts = append(atlStarts, cell{rows - 1, c})
	}
	pacific := flood(pacStarts)
	atlantic := flood(atlStarts)
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if pacific[r][c] && atlantic[r][c] {
				result = append(result, []int{r, c})
			}
		}
	}
	return result
}

func main() {
	fmt.Println(pacificAtlantic([][]int{[]int{1, 2}, []int{2, 1}}))
}
