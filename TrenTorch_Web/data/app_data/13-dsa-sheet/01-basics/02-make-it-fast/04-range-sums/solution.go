package main

import "fmt"

// O(n + q) time, O(n) space (prefix sums)
func rangeSums(nums []int, queries [][]int) []int {
	prefix := make([]int, len(nums)+1)
	for i, v := range nums {
		prefix[i+1] = prefix[i] + v
	}
	out := make([]int, 0, len(queries))
	for _, q := range queries {
		out = append(out, prefix[q[1]+1]-prefix[q[0]])
	}
	return out
}

func main() {
	fmt.Println(rangeSums([]int{1, 2, 3, 4, 5}, [][]int{[]int{0, 4}, []int{1, 3}, []int{2, 2}}))
}
