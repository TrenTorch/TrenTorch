package main

import (
	"fmt"
	"math/bits"
)

// O(1) time, O(1) space
func countDoublingSteps(n int) int {
	return bits.Len(uint(n - 1))
}

func main() {
	fmt.Println(countDoublingSteps(8))
}
