package main

import (
	"fmt"
	"math/big"
)

// O(n * S / 64) time where S is the total sum (big-int bitset), O(S) space
func canPartition(nums []int) bool {
	total := 0
	for _, x := range nums {
		total += x
	}
	if total%2 != 0 {
		return false
	}
	bits := big.NewInt(1)
	shifted := new(big.Int)
	for _, x := range nums {
		shifted.Lsh(bits, uint(x))
		bits.Or(bits, shifted)
	}
	return bits.Bit(total/2) == 1
}

func main() {
	fmt.Println(canPartition([]int{1, 5, 11, 5}))
}
