package main

import "fmt"

const mod = 1000000007

// fib returns (F(k), F(k+1)) modulo mod, using fast doubling.
func fib(k int) (int, int) {
	if k == 0 {
		return 0, 1
	}
	a, b := fib(k >> 1)
	t := (2*b - a) % mod
	if t < 0 {
		t += mod
	}
	c := a * t % mod
	d := (a*a + b*b) % mod
	if k&1 == 1 {
		return d, (c + d) % mod
	}
	return c, d
}

// O(log n) time, O(log n) space
func climbStairs(n int) int {
	f, _ := fib(n + 1)
	return f
}

func main() {
	fmt.Println(climbStairs(3))
}
