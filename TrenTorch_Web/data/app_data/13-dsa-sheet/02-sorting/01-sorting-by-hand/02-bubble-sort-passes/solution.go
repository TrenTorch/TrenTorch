package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space (Fenwick tree over value ranks; counts the passes bubble sort needs).
func bubbleSortPasses(nums []int) int {
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
	mostBiggerBefore := 0
	for seen, x := range nums {
		i := rank[x]
		notBigger := 0
		for i > 0 {
			notBigger += tree[i]
			i -= i & -i
		}
		if seen-notBigger > mostBiggerBefore {
			mostBiggerBefore = seen - notBigger
		}
		i = rank[x]
		for i <= size {
			tree[i]++
			i += i & -i
		}
	}
	return mostBiggerBefore + 1
}

func main() {
	fmt.Println(bubbleSortPasses([]int{3, 2, 1}))
}
