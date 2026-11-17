package main

import "fmt"

// O(n log(max nums)) time, O(1) space
func smallestDivisor(nums []int, threshold int) int {
	lo, hi := 1, 0
	for _, x := range nums {
		if x > hi {
			hi = x
		}
	}

	for lo < hi {
		mid := lo + (hi-lo)/2
		sum := 0
		for _, x := range nums {
			sum += (x + mid - 1) / mid
		}
		if sum <= threshold {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

func main() {
	fmt.Println(smallestDivisor([]int{1, 2, 5, 9}, 6))
}
