package main

import "fmt"

// O(n * k) time, O(k) space (or O(n) when k >= n/2)
func maxProfitK(k int, prices []int) int {
	const negInf = -(1 << 62)
	if k == 0 || len(prices) < 2 {
		return 0
	}
	if k >= len(prices)/2 {
		total := 0
		for i := 1; i < len(prices); i++ {
			total += max(0, prices[i]-prices[i-1])
		}
		return total
	}
	hold := make([]int, k+1)
	free := make([]int, k+1)
	for t := range hold {
		hold[t] = negInf
	}
	for _, p := range prices {
		for t := 1; t <= k; t++ {
			hold[t] = max(hold[t], free[t-1]-p)
			free[t] = max(free[t], hold[t]+p)
		}
	}
	return free[k]
}

func main() {
	fmt.Println(maxProfitK(2, []int{3, 2, 6, 5, 0, 3}))
}
