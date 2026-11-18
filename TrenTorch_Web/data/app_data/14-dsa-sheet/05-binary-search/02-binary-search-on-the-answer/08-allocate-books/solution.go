package main

import "fmt"

// O(n log(sum of pages)) time, O(1) space
func allocateBooks(pages []int, students int) int {
	if students > len(pages) {
		return -1
	}
	lo, hi := 0, 0
	for _, p := range pages {
		if p > lo {
			lo = p
		}
		hi += p
	}
	for lo < hi {
		mid := (lo + hi) / 2
		needed, load := 1, 0
		for _, p := range pages {
			if load+p > mid {
				needed++
				load = 0
			}
			load += p
		}
		if needed <= students {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func main() {
	fmt.Println(allocateBooks([]int{12, 34, 67, 90}, 2))
}
