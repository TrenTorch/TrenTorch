package main

import "fmt"

// O(1) time (32 bit positions), O(1) space
func longestOnesAfterFlip(n int) int {
	best, current, previous := 0, 0, 0
	for i := 0; i < 32; i++ {
		if ((n >> i) & 1) == 1 {
			current++
		} else {
			previous = current
			current = 0
		}
		if previous+current+1 > best {
			best = previous + current + 1
		}
	}
	if best > 32 {
		return 32
	}
	return best
}

func main() {
	fmt.Println(longestOnesAfterFlip(1775))
}
