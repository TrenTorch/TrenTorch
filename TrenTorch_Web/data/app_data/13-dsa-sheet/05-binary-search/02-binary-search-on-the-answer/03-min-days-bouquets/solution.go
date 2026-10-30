package main

import "fmt"

// O(n log(max bloom)) time, O(1) space
func minDaysBouquets(bloom []int, m int, k int) int {
	if m*k > len(bloom) {
		return -1
	}

	possible := func(day int) bool {
		bouquets, run := 0, 0
		for _, b := range bloom {
			if b <= day {
				run++
				if run == k {
					bouquets++
					run = 0
				}
			} else {
				run = 0
			}
		}
		return bouquets >= m
	}

	lo, hi := bloom[0], bloom[0]
	for _, b := range bloom {
		if b < lo {
			lo = b
		}
		if b > hi {
			hi = b
		}
	}

	for lo < hi {
		mid := lo + (hi-lo)/2
		if possible(mid) {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func main() {
	fmt.Println(minDaysBouquets([]int{1, 10, 3, 10, 2}, 3, 1))
}
