package main

import (
	"fmt"
	"math/bits"
)

// O(n log n) time and space to build, O(1) time per query
func rangeMinimums(nums []int, queries [][]int) []int {
	n := len(nums)
	table := [][]int{append([]int(nil), nums...)}
	for k := 1; 1<<k <= n; k++ {
		prev := table[len(table)-1]
		half := 1 << (k - 1)
		row := make([]int, len(prev)-half)
		for i := range row {
			row[i] = min(prev[i], prev[i+half])
		}
		table = append(table, row)
	}
	out := []int{}
	for _, q := range queries {
		left, right := q[0], q[1]
		level := bits.Len(uint(right-left+1)) - 1
		row := table[level]
		out = append(out, min(row[left], row[right-(1<<level)+1]))
	}
	return out
}

func main() {
	fmt.Println(rangeMinimums([]int{5, 2, 8, 1, 9}, [][]int{[]int{0, 4}, []int{1, 2}, []int{2, 2}}))
}
