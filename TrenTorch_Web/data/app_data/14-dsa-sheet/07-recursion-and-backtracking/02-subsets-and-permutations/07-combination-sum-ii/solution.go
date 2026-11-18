package main

import (
	"fmt"
	"sort"
)

// O(2^n) time in the worst case, O(total size of the output) space, O(n) extra space
func combinationSumIi(candidates []int, target int) [][]int {
	a := append([]int(nil), candidates...)
	sort.Ints(a)
	out := [][]int{}
	current := []int{}
	var gen func(start, remaining int)
	gen = func(start, remaining int) {
		if remaining == 0 {
			out = append(out, append([]int(nil), current...))
			return
		}
		for j := start; j < len(a); j++ {
			if j > start && a[j] == a[j-1] {
				continue
			}
			if a[j] > remaining {
				break
			}
			current = append(current, a[j])
			gen(j+1, remaining-a[j])
			current = current[:len(current)-1]
		}
	}
	gen(0, target)
	return out
}

func main() {
	fmt.Println(combinationSumIi([]int{10, 1, 2, 7, 6, 1, 5}, 8))
}
