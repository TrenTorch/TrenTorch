package main

import (
	"fmt"
	"math"
)

// O(k * E + n) time, O(n) space
func cheapestPrice(n int, flights [][]int, src int, dst int, k int) int {
	const inf = math.MaxInt
	best := make([]int, n)
	for i := range best {
		best[i] = inf
	}
	best[src] = 0
	for round := 0; round <= k; round++ {
		next := make([]int, n)
		copy(next, best)
		for _, f := range flights {
			a, b, price := f[0], f[1], f[2]
			if best[a] != inf && best[a]+price < next[b] {
				next[b] = best[a] + price
			}
		}
		best = next
	}
	if best[dst] == inf {
		return -1
	}
	return best[dst]
}

func main() {
	fmt.Println(cheapestPrice(4, [][]int{[]int{0, 1, 100}, []int{1, 2, 100}, []int{2, 0, 100}, []int{1, 3, 600}, []int{2, 3, 200}}, 0, 3, 1))
}
