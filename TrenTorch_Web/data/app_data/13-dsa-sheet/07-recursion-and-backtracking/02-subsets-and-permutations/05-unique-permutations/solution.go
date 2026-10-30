package main

import (
	"fmt"
	"sort"
)

// O(n! * n) time in the worst case, O(n! * n) space for the output, O(n) extra space
func uniquePermutations(nums []int) [][]int {
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
			if used[j] || (j > 0 && a[j] == a[j-1] && !used[j-1]) {
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
	fmt.Println(uniquePermutations([]int{1, 1, 2}))
}
