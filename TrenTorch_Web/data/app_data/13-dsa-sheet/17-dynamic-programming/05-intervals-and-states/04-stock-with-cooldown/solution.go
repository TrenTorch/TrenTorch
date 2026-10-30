package main

import "fmt"

// O(n) time, O(1) space
func maxProfitCooldown(prices []int) int {
	const negInf = -(1 << 62)
	hold, sold, rest := negInf, 0, 0
	for _, price := range prices {
		hold, sold, rest = max(hold, rest-price), hold+price, max(rest, sold)
	}
	return max(sold, rest)
}

func main() {
	fmt.Println(maxProfitCooldown([]int{1, 2, 3, 0, 2}))
}
