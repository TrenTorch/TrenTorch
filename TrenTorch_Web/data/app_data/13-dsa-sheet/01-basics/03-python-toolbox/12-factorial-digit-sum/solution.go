package main

import (
	"fmt"
	"math/big"
)

// O(n log n) time-ish via big-integer multiplication, O(d) space where d is the number of digits of n!.
func factorialDigitSum(n int) int {
	f := new(big.Int).MulRange(1, int64(n))
	sum := 0
	for _, ch := range f.String() {
		sum += int(ch - '0')
	}
	return sum
}

func main() {
	fmt.Println(factorialDigitSum(10))
}
