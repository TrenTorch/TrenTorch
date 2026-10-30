package main

import "fmt"

// O(p log(max pile)) time, O(1) space (p = len(piles))
func minEatingSpeed(piles []int, hours int) int {
	lo, hi := 1, 0
	for _, p := range piles {
		if p > hi {
			hi = p
		}
	}

	for lo < hi {
		mid := lo + (hi-lo)/2
		needed := 0
		for _, p := range piles {
			needed += (p + mid - 1) / mid
		}
		if needed <= hours {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func main() {
	fmt.Println(minEatingSpeed([]int{3, 6, 7, 11}, 8))
}
