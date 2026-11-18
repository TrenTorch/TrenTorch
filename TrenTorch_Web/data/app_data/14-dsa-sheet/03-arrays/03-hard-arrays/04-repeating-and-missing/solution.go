package main

import "fmt"

// O(n) time, O(1) space
func repeatingAndMissing(nums []int) []int {
	n := len(nums)
	sum, sumSq := 0, 0
	for _, x := range nums {
		sum += x
		sumSq += x * x
	}
	diff := sum - n*(n+1)/2
	squareDiff := sumSq - n*(n+1)*(2*n+1)/6
	plus := squareDiff / diff
	return []int{(plus + diff) / 2, (plus - diff) / 2}
}

func main() {
	fmt.Println(repeatingAndMissing([]int{3, 1, 2, 5, 3}))
}
