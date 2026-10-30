package main

import "fmt"

// O(n) time, O(1) space
func maxProfitMany(prices []int) int {
	total := 0
	for i := 1; i < len(prices); i++ {
		if d := prices[i] - prices[i-1]; d > 0 {
			total += d
		}
	}
	return total
}

func main() {
	fmt.Println(maxProfitMany([]int{7, 1, 5, 3, 6, 4}))
}
