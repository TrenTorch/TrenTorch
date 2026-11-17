package main

import (
	"fmt"
	"math/big"
)

// O(n*m) time for schoolbook big-int multiplication, O(n+m) space
func multiplyStrings(a string, b string) string {
	x, ok := new(big.Int).SetString(a, 10)
	if !ok {
		panic("multiplyStrings: invalid decimal string a: " + a)
	}
	y, ok := new(big.Int).SetString(b, 10)
	if !ok {
		panic("multiplyStrings: invalid decimal string b: " + b)
	}
	return new(big.Int).Mul(x, y).String()
}

func main() {
	fmt.Println(multiplyStrings("123", "456"))
}
