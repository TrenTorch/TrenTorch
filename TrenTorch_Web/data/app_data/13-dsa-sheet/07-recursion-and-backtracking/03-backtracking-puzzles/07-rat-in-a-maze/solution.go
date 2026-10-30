package main

import "fmt"

// O(4^(R*C)) worst-case time for enumerating paths, O(R * C) extra space
func ratInAMaze(maze [][]int) []string {
	out := []string{}
	rows := len(maze)
	cols := 0
	if rows > 0 {
		cols = len(maze[0])
	}
	if rows == 0 || cols == 0 || maze[0][0] == 0 || maze[rows-1][cols-1] == 0 {
		return out
	}
	onPath := make([][]bool, rows)
	for r := range onPath {
		onPath[r] = make([]bool, cols)
	}
	path := []byte{}
	moves := []struct {
		letter byte
		dr, dc int
	}{
		{'D', 1, 0},
		{'L', 0, -1},
		{'R', 0, 1},
		{'U', -1, 0},
	}
	var rec func(r, c int)
	rec = func(r, c int) {
		if r == rows-1 && c == cols-1 {
			out = append(out, string(path))
			return
		}
		onPath[r][c] = true
		for _, m := range moves {
			nr, nc := r+m.dr, c+m.dc
			if nr >= 0 && nr < rows && nc >= 0 && nc < cols && maze[nr][nc] == 1 && !onPath[nr][nc] {
				path = append(path, m.letter)
				rec(nr, nc)
				path = path[:len(path)-1]
			}
		}
		onPath[r][c] = false
	}
	rec(0, 0)
	return out
}

func main() {
	fmt.Println(ratInAMaze([][]int{[]int{1, 0, 0, 0}, []int{1, 1, 0, 1}, []int{1, 1, 0, 0}, []int{0, 1, 1, 1}}))
}
