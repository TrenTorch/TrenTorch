package main

import (
	"fmt"
	"math/bits"
)

// O(k log n) time with k = 12 fixed bases (deterministic for n < 3.3e24), O(1) space
func isPrime(n int) bool {
	if n < 2 {
		return false
	}
	small := []uint64{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}
	un := uint64(n)
	for _, p := range small {
		if un%p == 0 {
			return un == p
		}
	}
	d, s := un-1, 0
	for d%2 == 0 {
		d /= 2
		s++
	}
	for _, a := range small {
		x := powModU64(a, d, un)
		if x == 1 || x == un-1 {
			continue
		}
		composite := true
		for r := 0; r < s-1; r++ {
			x = mulModU64(x, x, un)
			if x == un-1 {
				composite = false
				break
			}
		}
		if composite {
			return false
		}
	}
	return true
}

// mulModU64 returns a*b mod m without overflow, for a, b < m.
func mulModU64(a, b, m uint64) uint64 {
	hi, lo := bits.Mul64(a, b)
	return bits.Rem64(hi, lo, m)
}

// powModU64 returns base^exp mod m.
func powModU64(base, exp, m uint64) uint64 {
	result := uint64(1) % m
	base %= m
	for exp > 0 {
		if exp&1 == 1 {
			result = mulModU64(result, base, m)
		}
		base = mulModU64(base, base, m)
		exp >>= 1
	}
	return result
}

func main() {
	fmt.Println(isPrime(97))
}
