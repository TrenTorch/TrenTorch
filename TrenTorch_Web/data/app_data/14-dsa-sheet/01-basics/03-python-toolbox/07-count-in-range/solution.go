package main

import (
	"fmt"
	"sort"
)

// O(q log n) time, O(q) space for the answers
func countInRange(sortedNums []int, queries [][]int) []int {
	out := make([]int, 0, len(queries))
	for _, q := range queries {
		lo, hi := q[0], q[1]
		// bisect_right(hi) equals the first index whose value is hi+1 or more
		out = append(out, sort.SearchInts(sortedNums, hi+1)-sort.SearchInts(sortedNums, lo))
	}
	return out
}

func main() {
	fmt.Println(countInRange([]int{1, 3, 3, 5, 8}, [][]int{[]int{3, 5}, []int{0, 0}, []int{2, 9}}))
}
