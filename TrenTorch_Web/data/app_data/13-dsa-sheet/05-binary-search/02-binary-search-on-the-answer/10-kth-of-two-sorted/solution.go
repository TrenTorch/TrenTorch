package main

import (
	"fmt"
	"math"
)

// O(log(min(m, n))) time, O(1) space
func kthOfTwoSorted(a []int, b []int, k int) int {
	if len(a) > len(b) {
		a, b = b, a
	}
	m, n := len(a), len(b)
	lo, hi := max(0, k-n), min(k, m)
	for lo <= hi {
		i := (lo + hi) / 2
		j := k - i
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
			return int(math.Max(aLeft, bLeft))
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
	fmt.Println(kthOfTwoSorted([]int{2, 3, 6, 7, 9}, []int{1, 4, 8, 10}, 5))
}
