package main

import "fmt"

// O(30 n) time, O(n) space (one prefix set per bit)
func maxXorPair(nums []int) int {
	best := 0
	for bit := 29; bit >= 0; bit-- {
		prefixes := make(map[int]bool, len(nums))
		for _, x := range nums {
			prefixes[x>>bit] = true
		}
		candidate := (best << 1) | 1
		best <<= 1
		for p := range prefixes {
			if prefixes[p^candidate] {
				best = candidate
				break
			}
		}
	}
	return best
}

func main() {
	fmt.Println(maxXorPair([]int{3, 10, 5, 25, 2, 8}))
}
