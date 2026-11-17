package main

import "fmt"

// O(n) time, O(1) space
func minCostClimbing(cost []int) int {
	prev2, prev1 := 0, 0
	for i := 2; i <= len(cost); i++ {
		prev2, prev1 = prev1, min(prev1+cost[i-1], prev2+cost[i-2])
	}
	return prev1
}

func main() {
	fmt.Println(minCostClimbing([]int{10, 15, 20}))
}
