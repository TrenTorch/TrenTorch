package main

import (
	"fmt"
	"sort"
)

// O(n + m + k log k) time, O(n + m) space (k = size of the result)
func commonValues(a []int, b []int) []int {
	inB := make(map[int]bool, len(b))
	for _, v := range b {
		inB[v] = true
	}

	seen := make(map[int]bool)
	result := []int{}
	for _, v := range a {
		if inB[v] && !seen[v] {
			seen[v] = true
			result = append(result, v)
		}
	}
	sort.Ints(result)
	return result
}

func main() {
	fmt.Println(commonValues([]int{1, 2, 2, 3}, []int{2, 2, 3, 4}))
}
