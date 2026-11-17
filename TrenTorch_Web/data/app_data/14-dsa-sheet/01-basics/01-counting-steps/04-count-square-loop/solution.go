package main

import (
	"fmt"
	"math"
)

// O(1) time, O(1) space
func countSquareLoop(n int) int {
	r := int(math.Sqrt(float64(n)))
	for r*r > n {
		r--
	}
	for (r+1)*(r+1) <= n {
		r++
	}
	return r
}

func main() {
	fmt.Println(countSquareLoop(10))
}
