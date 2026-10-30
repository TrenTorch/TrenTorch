package main

import (
	"fmt"
	"sort"
)

// O(n^3) time, O(n^2) space, where n = len(cuts) + 2
func minCostCut(length int, cuts []int) int {
	sortedCuts := make([]int, len(cuts))
	copy(sortedCuts, cuts)
	sort.Ints(sortedCuts)
	points := make([]int, 0, len(cuts)+2)
	points = append(points, 0)
	points = append(points, sortedCuts...)
	points = append(points, length)
	n := len(points)
	dp := make([][]int, n)
	bestCut := make([][]int, n)
	for i := range dp {
		dp[i] = make([]int, n)
		bestCut[i] = make([]int, n)
	}
	for i := 0; i < n-1; i++ {
		bestCut[i][i+1] = i + 1
	}
	for span := 2; span < n; span++ {
		for i := 0; i < n-span; i++ {
			j := i + span
			low := max(i+1, bestCut[i][j-1])
			high := min(j-1, bestCut[i+1][j])
			best := -1
			for k := low; k <= high; k++ {
				value := dp[i][k] + dp[k][j]
				if best < 0 || value < best {
					best = value
					bestCut[i][j] = k
				}
			}
			dp[i][j] = best + points[j] - points[i]
		}
	}
	return dp[0][n-1]
}

func main() {
	fmt.Println(minCostCut(7, []int{1, 3, 4, 5}))
}
