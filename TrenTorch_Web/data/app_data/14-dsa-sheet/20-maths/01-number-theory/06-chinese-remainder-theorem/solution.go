package main

import "fmt"

// O(k log M) time for k congruences and modulus M, O(1) space
func solveCongruences(remainders []int, moduli []int) int {
	x, modulus := 0, 1
	for i, m := range moduli {
		r := remainders[i]
		g := gcdInt(modulus, m)
		if (r-x)%g != 0 {
			return -1
		}
		lcm := modulus / g * m
		mg := m / g
		inv := invModInt(modulus/g, mg)
		t := ((r - x) / g % mg) * inv % mg
		if t < 0 {
			t += mg
		}
		x = (x + modulus*t) % lcm
		modulus = lcm
	}
	return x
}

func gcdInt(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// invModInt returns the inverse of a modulo m, assuming gcd(a, m) = 1.
func invModInt(a, m int) int {
	if m == 1 {
		return 0
	}
	oldR, r := ((a%m)+m)%m, m
	oldX, x := 1, 0
	for r != 0 {
		q := oldR / r
		oldR, r = r, oldR-q*r
		oldX, x = x, oldX-q*x
	}
	return ((oldX % m) + m) % m
}

func main() {
	fmt.Println(solveCongruences([]int{2, 3, 2}, []int{3, 5, 7}))
}
