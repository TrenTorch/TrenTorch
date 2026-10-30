package main

import "fmt"

// O(length^2) time, O(length) space
func rodCutting(prices []int, length int) int {
	best := make([]int, length+1)
	for n := 1; n <= length; n++ {
		for k := 1; k <= n; k++ {
			if prices[k-1]+best[n-k] > best[n] {
				best[n] = prices[k-1] + best[n-k]
			}
		}
	}
	return best[length]
}

func main() {
	fmt.Println(rodCutting([]int{1, 5, 8, 9, 10, 17, 17, 20}, 8))
}
