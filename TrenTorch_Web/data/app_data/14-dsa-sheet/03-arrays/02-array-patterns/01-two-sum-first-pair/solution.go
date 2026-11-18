package main

import "fmt"

// O(n) time, O(n) space
func twoSumFirstPair(nums []int, target int) []int {
	first := map[int]int{}
	found := false
	best := [2]int{-1, -1}
	for j, x := range nums {
		if i, ok := first[target-x]; ok {
			if !found || i < best[0] || (i == best[0] && j < best[1]) {
				best = [2]int{i, j}
				found = true
			}
		}
		if _, ok := first[x]; !ok {
			first[x] = j
		}
	}
	return []int{best[0], best[1]}
}

func main() {
	fmt.Println(twoSumFirstPair([]int{1, 6, 5, 3, 8}, 9))
}
