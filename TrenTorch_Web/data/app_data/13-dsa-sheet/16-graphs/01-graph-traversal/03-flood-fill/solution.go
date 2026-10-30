package main

import "fmt"

type cell struct{ r, c int }

// O(R*C) time, O(R*C) space
func floodFill(image [][]int, sr int, sc int, color int) [][]int {
	old := image[sr][sc]
	if old == color {
		return image
	}
	rows, cols := len(image), len(image[0])
	image[sr][sc] = color
	stack := []cell{{sr, sc}}
	for len(stack) > 0 {
		cur := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		for _, d := range [4]cell{{cur.r + 1, cur.c}, {cur.r - 1, cur.c}, {cur.r, cur.c + 1}, {cur.r, cur.c - 1}} {
			if d.r >= 0 && d.r < rows && d.c >= 0 && d.c < cols && image[d.r][d.c] == old {
				image[d.r][d.c] = color
				stack = append(stack, d)
			}
		}
	}
	return image
}

func main() {
	fmt.Println(floodFill([][]int{[]int{1, 1, 1}, []int{1, 1, 0}, []int{1, 0, 1}}, 1, 1, 2))
}
