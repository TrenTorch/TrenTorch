package main

import (
	"fmt"
	"math"
)

// O(sqrt(n)) time, O(1) space
func sumDivisorCounts(n int) int {
	r := int(math.Sqrt(float64(n)))
	for r*r > n {
		r--
	}
	for (r+1)*(r+1) <= n {
		r++
	}
	sum := 0
	for j := 1; j <= r; j++ {
		sum += n / j
	}
	return 2*sum - r*r
}

func main() {
	fmt.Println(sumDivisorCounts(5))
}
