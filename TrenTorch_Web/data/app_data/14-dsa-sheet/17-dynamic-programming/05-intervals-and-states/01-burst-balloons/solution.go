package main

import "fmt"

// O(n^3) time, O(n^2) space (n = len(nums) + 2)
func maxCoins(nums []int) int {
	a := make([]int, 0, len(nums)+2)
	a = append(a, 1)
	a = append(a, nums...)
	a = append(a, 1)
	n := len(a)
	dp := make([][]int, n)
	for i := range dp {
		dp[i] = make([]int, n)
	}
	for length := 2; length < n; length++ {
		for i := 0; i < n-length; i++ {
			j := i + length
			best := 0
			for k := i + 1; k < j; k++ {
				value := dp[i][k] + dp[k][j] + a[i]*a[k]*a[j]
				if value > best {
					best = value
				}
			}
			dp[i][j] = best
		}
	}
	return dp[0][n-1]
}

func main() {
	fmt.Println(maxCoins([]int{3, 1, 5, 8}))
}
