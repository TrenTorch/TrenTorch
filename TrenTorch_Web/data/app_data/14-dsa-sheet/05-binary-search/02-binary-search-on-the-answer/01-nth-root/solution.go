package main

import (
	"fmt"
	"math/bits"
)

// powCmp compares x**m with n without overflowing: -1 if x**m < n, 0 if equal, 1 if greater.
// x must be >= 1.
func powCmp(x, m, n int) int {
	result := 1
	for i := 0; i < m; i++ {
		if result > n/x {
			return 1
		}
		result *= x
	}
	switch {
	case result == n:
		return 0
	case result < n:
		return -1
	default:
		return 1
	}
}

// O(log n * m) time, O(1) space
func nthRoot(n int, m int) int {
	lo, hi := 1, 1<<(bits.Len(uint(n))/m+1)
	for lo <= hi {
		mid := lo + (hi-lo)/2
		c := powCmp(mid, m, n)
		if c == 0 {
			return mid
		}
		if c < 0 {
			lo = mid + 1
		} else {
			hi = mid - 1
		}
	}
	return -1
}

func main() {
	fmt.Println(nthRoot(27, 3))
}
