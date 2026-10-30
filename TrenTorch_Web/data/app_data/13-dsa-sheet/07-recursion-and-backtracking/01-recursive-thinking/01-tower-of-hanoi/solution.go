package main

import "fmt"

// O(2^n) time, O(2^n) space (the output has 2^n - 1 moves)
func towerOfHanoi(n int) [][]int {
	moves := make([][]int, 0, (1<<n)-1)
	var move func(k, source, target, spare int)
	move = func(k, source, target, spare int) {
		if k == 0 {
			return
		}
		move(k-1, source, spare, target)
		moves = append(moves, []int{source, target})
		move(k-1, spare, target, source)
	}
	move(n, 1, 3, 2)
	return moves
}

func main() {
	fmt.Println(towerOfHanoi(2))
}
