package main

import "fmt"

// O(amount * len(coins)) time, O(amount) space
func coinChange(coins []int, amount int) int {
	const inf = int(^uint(0) >> 1)
	best := make([]int, amount+1)
	for a := 1; a <= amount; a++ {
		best[a] = inf
	}
	for a := 1; a <= amount; a++ {
		for _, c := range coins {
			if c <= a && best[a-c] != inf && best[a-c]+1 < best[a] {
				best[a] = best[a-c] + 1
			}
		}
	}
	if best[amount] == inf {
		return -1
	}
	return best[amount]
}

func main() {
	fmt.Println(coinChange([]int{1, 2, 5}, 11))
}
