package main

import (
	"fmt"
	"sort"
)

// O(n^(target/min) ) time in the worst case, O(target * number of results) space for the output, O(target) extra space
func combinationSum(candidates []int, target int) [][]int {
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
			if a[j] > remaining {
				break
			}
			current = append(current, a[j])
			gen(j, remaining-a[j])
			current = current[:len(current)-1]
		}
	}
	gen(0, target)
	return out
}

func main() {
	fmt.Println(combinationSum([]int{2, 3, 6, 7}, 7))
}
