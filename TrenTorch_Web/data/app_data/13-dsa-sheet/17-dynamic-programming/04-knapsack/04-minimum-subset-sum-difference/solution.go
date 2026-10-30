package main

import (
	"fmt"
	"math/big"
)

// O(n * total / 64) time, O(total) space (big.Int bitset)
func minSubsetDifference(nums []int) int {
	total := 0
	for _, x := range nums {
		total += x
	}
	bits := big.NewInt(1)
	for _, x := range nums {
		shifted := new(big.Int).Lsh(bits, uint(x))
		bits.Or(bits, shifted)
	}
	for s := total / 2; s >= 0; s-- {
		if bits.Bit(s) == 1 {
			return total - 2*s
		}
	}
	return total
}

func main() {
	fmt.Println(minSubsetDifference([]int{1, 6, 11, 5}))
}
