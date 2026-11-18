package main

import "fmt"

type pathState struct{ x, y, steps int }

// O(R*C) time, O(R*C) space
func shortestPathBinaryMatrix(grid [][]int) int {
	rows := len(grid)
	cols := 0
	if rows > 0 {
		cols = len(grid[0])
	}
	if rows == 0 || cols == 0 || grid[0][0] == 1 || grid[rows-1][cols-1] == 1 {
		return -1
	}
	seen := make([][]bool, rows)
	for i := range seen {
		seen[i] = make([]bool, cols)
	}
	seen[0][0] = true
	queue := []pathState{{0, 0, 1}}
	for head := 0; head < len(queue); head++ {
		cur := queue[head]
		if cur.x == rows-1 && cur.y == cols-1 {
			return cur.steps
		}
		for dx := -1; dx <= 1; dx++ {
			for dy := -1; dy <= 1; dy++ {
				nx, ny := cur.x+dx, cur.y+dy
				if nx >= 0 && nx < rows && ny >= 0 && ny < cols && grid[nx][ny] == 0 && !seen[nx][ny] {
					seen[nx][ny] = true
					queue = append(queue, pathState{nx, ny, cur.steps + 1})
				}
			}
		}
	}
	return -1
}

func main() {
	fmt.Println(shortestPathBinaryMatrix([][]int{[]int{0, 0, 0}, []int{1, 1, 0}, []int{1, 1, 0}}))
}
