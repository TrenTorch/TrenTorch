package main

import "fmt"

// O(rows * cols) time, O(cols) space
func calculateMinimumHp(dungeon [][]int) int {
	rows := len(dungeon)
	cols := 0
	if rows > 0 {
		cols = len(dungeon[0])
	}
	if rows == 0 || cols == 0 {
		return 1
	}
	const inf = 1 << 62
	need := make([]int, cols+1)
	for i := range need {
		need[i] = inf
	}
	need[cols-1] = 1
	for r := rows - 1; r >= 0; r-- {
		for c := cols - 1; c >= 0; c-- {
			bestNext := min(need[c], need[c+1])
			if r == rows-1 && c == cols-1 {
				bestNext = 1
			}
			need[c] = max(1, bestNext-dungeon[r][c])
		}
		need[cols] = inf
	}
	return need[0]
}

func main() {
	fmt.Println(calculateMinimumHp([][]int{[]int{-2, -3, 3}, []int{-5, -10, 1}, []int{10, 30, -5}}))
}
