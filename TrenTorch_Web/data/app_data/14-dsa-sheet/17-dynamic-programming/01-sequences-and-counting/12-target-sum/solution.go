package main

import "fmt"

// O(n * D) time where D is the number of distinct partial sums, O(D) space
func findTargetSumWays(nums []int, target int) int {
	ways := map[int]int{0: 1}
	for _, x := range nums {
		nxt := map[int]int{}
		for s, count := range ways {
			nxt[s+x] += count
			nxt[s-x] += count
		}
		ways = nxt
	}
	return ways[target]
}

func main() {
	fmt.Println(findTargetSumWays([]int{1, 1, 1, 1, 1}, 3))
}
