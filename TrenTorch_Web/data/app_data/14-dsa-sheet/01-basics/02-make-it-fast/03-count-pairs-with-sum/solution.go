package main

import "fmt"

// O(n) time, O(n) space
func countPairsWithSum(nums []int, target int) int {
	seen := make(map[int]int)
	count := 0
	for _, x := range nums {
		count += seen[target-x]
		seen[x]++
	}
	return count
}

func main() {
	fmt.Println(countPairsWithSum([]int{1, 2, 3, 4, 3}, 6))
}
