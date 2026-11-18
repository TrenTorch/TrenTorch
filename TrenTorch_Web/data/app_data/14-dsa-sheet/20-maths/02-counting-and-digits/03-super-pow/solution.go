package main

import "fmt"

// O(len(b) * log 10) time, O(1) space
func superPow(a int, b []int) int {
	const mod = 1337
	result := 1
	for _, digit := range b {
		result = powModInt(result, 10, mod) * powModInt(a, digit, mod) % mod
	}
	return result
}

// powModInt returns base^exp mod m for non-negative exp.
func powModInt(base, exp, m int) int {
	result := 1 % m
	base %= m
	for exp > 0 {
		if exp&1 == 1 {
			result = result * base % m
		}
		base = base * base % m
		exp >>= 1
	}
	return result
}

func main() {
	fmt.Println(superPow(2, []int{1, 0}))
}
