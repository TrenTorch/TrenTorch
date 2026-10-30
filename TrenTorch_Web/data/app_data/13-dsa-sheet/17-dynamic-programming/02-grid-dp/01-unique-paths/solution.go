package main

import (
	"fmt"
	"math/big"
)

// O(min(rows, cols)) big-int steps time, O(min(rows, cols)) space
func uniquePaths(rows int, cols int) int {
	const mod = 1000000007
	c := new(big.Int).Binomial(int64(rows+cols-2), int64(rows-1))
	c.Mod(c, big.NewInt(mod))
	return int(c.Int64())
}

func main() {
	fmt.Println(uniquePaths(3, 7))
}
