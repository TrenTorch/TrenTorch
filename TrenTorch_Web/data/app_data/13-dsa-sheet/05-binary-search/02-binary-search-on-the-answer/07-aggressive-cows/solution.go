package main

import (
	"fmt"
	"sort"
)

// O(n log n + n log(max gap)) time, O(n) space
func aggressiveCows(stalls []int, cows int) int {
	s := make([]int, len(stalls))
	copy(s, stalls)
	sort.Ints(s)

	canPlace := func(distance int) bool {
		placed, last := 1, s[0]
		for _, position := range s[1:] {
			if position-last >= distance {
				placed++
				last = position
			}
		}
		return placed >= cows
	}

	lo, hi := 1, s[len(s)-1]-s[0]
	for lo < hi {
		mid := (lo + hi + 1) / 2
		if canPlace(mid) {
			lo = mid
		} else {
			hi = mid - 1
		}
	}
	return lo
}

func main() {
	fmt.Println(aggressiveCows([]int{1, 2, 4, 8, 9}, 3))
}
