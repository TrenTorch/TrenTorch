package main

import (
	"fmt"
	"sort"
)

// O(n! * n) time, O(n! * n) space for the output, O(n) extra space
func allPermutations(nums []int) [][]int {
	a := append([]int(nil), nums...)
	sort.Ints(a)
	used := make([]bool, len(a))
	out := [][]int{}
	current := []int{}
	var gen func()
	gen = func() {
		if len(current) == len(a) {
			out = append(out, append([]int(nil), current...))
			return
		}
		for j := range a {
			if used[j] {
				continue
			}
			used[j] = true
			current = append(current, a[j])
			gen()
			current = current[:len(current)-1]
			used[j] = false
		}
	}
	gen()
	return out
}

func main() {
	fmt.Println(allPermutations([]int{1, 2, 3}))
}
