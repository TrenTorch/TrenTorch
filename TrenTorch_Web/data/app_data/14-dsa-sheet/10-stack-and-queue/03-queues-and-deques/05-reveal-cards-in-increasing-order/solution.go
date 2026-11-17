package main

import (
	"fmt"
	"sort"
)

// O(n log n) time (sorting), O(n) space
func revealCards(deck []int) []int {
	n := len(deck)
	result := make([]int, n)
	sorted := make([]int, n)
	copy(sorted, deck)
	sort.Ints(sorted)
	positions := make([]int, n)
	for i := range positions {
		positions[i] = i
	}
	head := 0
	for _, card := range sorted {
		result[positions[head]] = card
		head++
		if head < len(positions) {
			positions = append(positions, positions[head])
			head++
		}
	}
	return result
}

func main() {
	fmt.Println(revealCards([]int{17, 13, 11, 2, 3, 5, 7}))
}
