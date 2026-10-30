package main

import "fmt"

// O(amount * len(coins)) time, O(amount) space
func countChange(amount int, coins []int) int {
	const mod = 1000000007
	ways := make([]int, amount+1)
	ways[0] = 1
	for _, c := range coins {
		for a := c; a <= amount; a++ {
			ways[a] = (ways[a] + ways[a-c]) % mod
		}
	}
	return ways[amount]
}

func main() {
	fmt.Println(countChange(5, []int{1, 2, 5}))
}
