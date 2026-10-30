package main

import "fmt"

// fibPair returns (F(k), F(k+1)) using fast doubling.
func fibPair(k int) (int, int) {
	if k == 0 {
		return 0, 1
	}
	a, b := fibPair(k >> 1)
	c := a * (2*b - a)
	d := a*a + b*b
	if k&1 == 1 {
		return d, c + d
	}
	return c, d
}

// O(log n) time, O(log n) space (recursion depth)
func nthFibonacci(n int) int {
	f, _ := fibPair(n)
	return f
}

func main() {
	fmt.Println(nthFibonacci(10))
}
