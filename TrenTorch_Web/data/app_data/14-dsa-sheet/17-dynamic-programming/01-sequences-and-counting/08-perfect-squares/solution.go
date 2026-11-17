package main

import (
	"fmt"
	"math"
)

// isqrt returns the integer square root of n (n >= 0).
func isqrt(n int) int {
	r := int(math.Sqrt(float64(n)))
	for r*r > n {
		r--
	}
	for (r+1)*(r+1) <= n {
		r++
	}
	return r
}

// O(sqrt(n) * log n) time, O(1) space
func numSquares(n int) int {
	if n == 0 {
		return 0
	}
	if isqrt(n)*isqrt(n) == n {
		return 1
	}
	m := n
	for m%4 == 0 {
		m /= 4
	}
	if m%8 == 7 {
		return 4
	}
	for i := 1; i*i <= n; i++ {
		rest := n - i*i
		if isqrt(rest)*isqrt(rest) == rest {
			return 2
		}
	}
	return 3
}

func main() {
	fmt.Println(numSquares(12))
}
