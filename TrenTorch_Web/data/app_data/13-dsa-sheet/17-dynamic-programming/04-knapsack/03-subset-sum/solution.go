package main

import (
	"fmt"
	"math/big"
)

// O(n * target / 64) time, O(target) space (big.Int bitset)
func subsetSum(nums []int, target int) bool {
	mask := new(big.Int).Lsh(big.NewInt(1), uint(target+1))
	mask.Sub(mask, big.NewInt(1))
	bits := big.NewInt(1)
	for _, x := range nums {
		shifted := new(big.Int).Lsh(bits, uint(x))
		shifted.And(shifted, mask)
		bits.Or(bits, shifted)
	}
	shifted := new(big.Int).Rsh(bits, uint(target))
	return shifted.Bit(0) == 1
}

func main() {
	fmt.Println(subsetSum([]int{3, 34, 4, 12, 5, 2}, 9))
}
