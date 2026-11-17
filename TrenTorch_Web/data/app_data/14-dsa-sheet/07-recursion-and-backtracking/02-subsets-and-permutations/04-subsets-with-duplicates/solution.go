package main

import (
	"fmt"
	"sort"
)

// O(n * 2^n) time, O(n * 2^n) space for the output in the worst case, O(n) extra space
func subsetsWithDuplicates(nums []int) [][]int {
	a := append([]int(nil), nums...)
	sort.Ints(a)
	out := [][]int{}
	current := []int{}
	var gen func(start int)
	gen = func(start int) {
		out = append(out, append([]int(nil), current...))
		for j := start; j < len(a); j++ {
			if j > start && a[j] == a[j-1] {
				continue
			}
			current = append(current, a[j])
			gen(j + 1)
			current = current[:len(current)-1]
		}
	}
	gen(0)
	return out
}

func main() {
	fmt.Println(subsetsWithDuplicates([]int{1, 2, 2}))
}
