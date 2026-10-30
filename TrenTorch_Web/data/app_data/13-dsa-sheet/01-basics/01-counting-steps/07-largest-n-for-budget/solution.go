package main

import (
	"fmt"
	"math/bits"
)

// saturatedMul returns a*b capped at budget+1. Anything above budget is
// reported as budget+1, so comparisons with budget stay exact and nothing overflows.
func saturatedMul(a, b, budget int) int {
	if a == 0 || b == 0 {
		return 0
	}
	limit := budget + 1
	if a > limit/b {
		return limit
	}
	p := a * b
	if p > limit {
		return limit
	}
	return p
}

func cost(growth string, n, budget int) int {
	switch growth {
	case "n":
		return n
	case "n log n":
		return saturatedMul(n, bits.Len(uint(n))-1, budget)
	case "n^2":
		return saturatedMul(n, n, budget)
	default:
		return saturatedMul(saturatedMul(n, n, budget), n, budget)
	}
}

// O(log budget) time, O(1) space (binary search over n)
func largestN(growth string, budget int) int {
	if growth == "2^n" {
		if budget >= 2 {
			return bits.Len(uint(budget)) - 1
		}
		return 0
	}
	if cost(growth, 1, budget) > budget {
		return 0
	}
	lo, hi := 1, budget+1
	for lo < hi {
		mid := (lo + hi + 1) / 2
		if cost(growth, mid, budget) <= budget {
			lo = mid
		} else {
			hi = mid - 1
		}
	}
	return lo
}

func main() {
	fmt.Println(largestN("n^2", 100))
}
