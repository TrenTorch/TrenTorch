package main

import "fmt"

// O(log n) time, O(log n) space (recursion depth)
func fibMod(n int) int {
	f, _ := fibPair(n)
	return f
}

// fibPair returns (F(k), F(k+1)) modulo 10^9 + 7, using fast doubling.
func fibPair(k int) (int, int) {
	const mod = 1000000007
	if k == 0 {
		return 0, 1
	}
	a, b := fibPair(k / 2)
	c := a * ((2*b - a + mod) % mod) % mod
	e := (a*a + b*b) % mod
	if k%2 == 1 {
		return e, (c + e) % mod
	}
	return c, e
}

func main() {
	fmt.Println(fibMod(10))
}
