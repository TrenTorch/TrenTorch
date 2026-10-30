package main

import "fmt"

// O(n^2) time, O(n^2) space for the n-1 snapshots of length n.
func selectionSortPasses(nums []int) [][]int {
	a := append([]int(nil), nums...)
	passes := [][]int{}
	for i := 0; i < len(a)-1; i++ {
		smallest := i
		for j := i + 1; j < len(a); j++ {
			if a[j] < a[smallest] {
				smallest = j
			}
		}
		a[i], a[smallest] = a[smallest], a[i]
		passes = append(passes, append([]int(nil), a...))
	}
	return passes
}

func main() {
	fmt.Println(selectionSortPasses([]int{64, 25, 12, 22, 11}))
}
