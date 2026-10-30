package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space (Fenwick tree over value ranks; counts the shifts insertion sort makes).
func insertionSortShifts(nums []int) int {
	sorted := append([]int(nil), nums...)
	sort.Ints(sorted)
	rank := make(map[int]int)
	for _, v := range sorted {
		if _, ok := rank[v]; !ok {
			rank[v] = len(rank) + 1
		}
	}
	size := len(rank)
	tree := make([]int, size+1)
	shifts := 0
	for seen, x := range nums {
		i := rank[x]
		notBigger := 0
		for i > 0 {
			notBigger += tree[i]
			i -= i & -i
		}
		shifts += seen - notBigger
		i = rank[x]
		for i <= size {
			tree[i]++
			i += i & -i
		}
	}
	return shifts
}

func main() {
	fmt.Println(insertionSortShifts([]int{3, 1, 2}))
}
