package main

import "fmt"

// O(n log(sum of weights)) time, O(1) space
func shipCapacity(weights []int, days int) int {
	lo, hi := 0, 0
	for _, w := range weights {
		if w > lo {
			lo = w
		}
		hi += w
	}

	for lo < hi {
		mid := lo + (hi-lo)/2
		needed, load := 1, 0
		for _, w := range weights {
			if load+w > mid {
				needed++
				load = 0
			}
			load += w
		}
		if needed <= days {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func main() {
	fmt.Println(shipCapacity([]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, 5))
}
