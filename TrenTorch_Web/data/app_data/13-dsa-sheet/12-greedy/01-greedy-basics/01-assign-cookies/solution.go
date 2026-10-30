package main

import (
	"fmt"
	"sort"
)

// O(n log n + m log m) time, O(n + m) space
func assignCookies(greed []int, sizes []int) int {
	g := append([]int(nil), greed...)
	s := append([]int(nil), sizes...)
	sort.Ints(g)
	sort.Ints(s)
	child := 0
	for _, cookie := range s {
		if child < len(g) && g[child] <= cookie {
			child++
		}
	}
	return child
}

func main() {
	fmt.Println(assignCookies([]int{1, 2, 3}, []int{1, 1}))
}
