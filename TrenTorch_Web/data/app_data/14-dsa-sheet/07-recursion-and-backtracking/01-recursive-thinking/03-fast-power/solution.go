package main

import "fmt"

// O(log exp) time, O(1) space
func powerMod(base int, exp int, mod int) int {
	result := 1 % mod
	base %= mod
	for exp != 0 {
		if (exp & 1) == 1 {
			result = result * base % mod
		}
		base = base * base % mod
		exp >>= 1
	}
	return result
}

func main() {
	fmt.Println(powerMod(2, 10, 1000))
}
