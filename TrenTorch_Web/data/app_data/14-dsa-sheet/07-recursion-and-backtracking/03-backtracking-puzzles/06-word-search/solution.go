package main

import "fmt"

// O(R * C * 4^L) time for word length L, O(R * C) space
func wordSearch(board []string, word string) bool {
	if len(word) == 0 {
		return true
	}
	rows := len(board)
	cols := 0
	if rows > 0 {
		cols = len(board[0])
	}
	grid := make([][]byte, rows)
	for r := range board {
		grid[r] = []byte(board[r])
	}
	var rec func(r, c, i int) bool
	rec = func(r, c, i int) bool {
		if i == len(word) {
			return true
		}
		if r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != word[i] {
			return false
		}
		saved := grid[r][c]
		grid[r][c] = '#'
		found := rec(r+1, c, i+1) || rec(r-1, c, i+1) || rec(r, c+1, i+1) || rec(r, c-1, i+1)
		grid[r][c] = saved
		return found
	}
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if rec(r, c, 0) {
				return true
			}
		}
	}
	return false
}

func main() {
	fmt.Println(wordSearch([]string{"abce", "sfcs", "adee"}, "abcced"))
}
