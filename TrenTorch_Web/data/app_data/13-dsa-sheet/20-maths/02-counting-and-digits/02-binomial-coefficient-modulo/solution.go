package main

import "fmt"

// O(min(k, n-k) + log mod) time, O(1) space
func binomialMod(n int, k int) int {
	const mod = 1000000007
	if k < 0 || k > n {
		return 0
	}
	if n-k < k {
		k = n - k
	}
	num, den := 1, 1
	for i := 0; i < k; i++ {
		num = num * ((n - i) % mod) % mod
		den = den * (i + 1) % mod
	}
	return num * powModInt(den, mod-2, mod) % mod
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
	fmt.Println(binomialMod(5, 2))
}
