package main

import "fmt"

// O(n) time, O(1) space
func stockBestProfit(prices []int) int {
	best := 0
	lowest := 0
	hasLowest := false
	for _, price := range prices {
		if hasLowest {
			best = max(best, price-lowest)
			lowest = min(lowest, price)
		} else {
			lowest = price
			hasLowest = true
		}
	}
	return best
}

func main() {
	fmt.Println(stockBestProfit([]int{7, 1, 5, 3, 6, 4}))
}
