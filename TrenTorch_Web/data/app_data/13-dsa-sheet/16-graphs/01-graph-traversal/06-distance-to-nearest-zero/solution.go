package main

import "fmt"

type cell struct{ r, c int }

// O(R*C) time, O(R*C) space
func nearestZero(mat [][]int) [][]int {
	rows := len(mat)
	cols := 0
	if rows > 0 {
		cols = len(mat[0])
	}
	dist := make([][]int, rows)
	queue := []cell{}
	for r := 0; r < rows; r++ {
		dist[r] = make([]int, cols)
		for c := 0; c < cols; c++ {
			dist[r][c] = -1
			if mat[r][c] == 0 {
				dist[r][c] = 0
				queue = append(queue, cell{r, c})
			}
		}
	}
	for head := 0; head < len(queue); head++ {
		cur := queue[head]
		for _, d := range [4]cell{{cur.r + 1, cur.c}, {cur.r - 1, cur.c}, {cur.r, cur.c + 1}, {cur.r, cur.c - 1}} {
			if d.r >= 0 && d.r < rows && d.c >= 0 && d.c < cols && dist[d.r][d.c] == -1 {
				dist[d.r][d.c] = dist[cur.r][cur.c] + 1
				queue = append(queue, d)
			}
		}
	}
	return dist
}

func main() {
	fmt.Println(nearestZero([][]int{[]int{0, 0, 0}, []int{0, 1, 0}, []int{1, 1, 1}}))
}
