package main

import (
	"fmt"
	"math"
)

// O(log(min(m, n))) time, O(1) space
func medianTwoSorted(a []int, b []int) float64 {
	if len(a) > len(b) {
		a, b = b, a
	}
	m, n := len(a), len(b)
	half := (m + n + 1) / 2
	lo, hi := 0, m
	for lo <= hi {
		i := (lo + hi) / 2
		j := half - i
		aLeft := math.Inf(-1)
		if i > 0 {
			aLeft = float64(a[i-1])
		}
		aRight := math.Inf(1)
		if i < m {
			aRight = float64(a[i])
		}
		bLeft := math.Inf(-1)
		if j > 0 {
			bLeft = float64(b[j-1])
		}
		bRight := math.Inf(1)
		if j < n {
			bRight = float64(b[j])
		}
		if aLeft <= bRight && bLeft <= aRight {
			if (m+n)%2 == 1 {
				return math.Max(aLeft, bLeft)
			}
			return (math.Max(aLeft, bLeft) + math.Min(aRight, bRight)) / 2
		}
		if aLeft > bRight {
			hi = i - 1
		} else {
			lo = i + 1
		}
	}
	return 0
}

func main() {
	fmt.Println(medianTwoSorted([]int{1, 3}, []int{2}))
}
