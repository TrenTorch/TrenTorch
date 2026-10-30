package main

import "fmt"

// O(n^3) time, O(n^2) space
func matrixChainCost(dims []int) int {
	n := len(dims)
	if n < 3 {
		return 0
	}
	inf := int(^uint(0) >> 1)
	dp := make([][]int, n)
	for i := range dp {
		dp[i] = make([]int, n)
	}
	for length := 2; length < n; length++ {
		for i := 0; i < n-length; i++ {
			j := i + length
			best := inf
			for k := i + 1; k < j; k++ {
				value := dp[i][k] + dp[k][j] + dims[i]*dims[k]*dims[j]
				if value < best {
					best = value
				}
			}
			dp[i][j] = best
		}
	}
	return dp[0][n-1]
}

func main() {
	fmt.Println(matrixChainCost([]int{10, 30, 5, 60}))
}
