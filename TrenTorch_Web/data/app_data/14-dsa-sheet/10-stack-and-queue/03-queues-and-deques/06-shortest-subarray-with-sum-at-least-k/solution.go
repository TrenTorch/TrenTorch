package main

import "fmt"

// O(n) time, O(n) space
func shortestSubarraySumK(nums []int, k int) int {
	n := len(nums)
	prefix := make([]int, n+1)
	for i, x := range nums {
		prefix[i+1] = prefix[i] + x
	}
	best := n + 1
	window := []int{}
	head := 0
	for b, p := range prefix {
		for len(window) > head && p-prefix[window[head]] >= k {
			best = min(best, b-window[head])
			head++
		}
		for len(window) > head && prefix[window[len(window)-1]] >= p {
			window = window[:len(window)-1]
		}
		window = append(window, b)
	}
	if best <= n {
		return best
	}
	return -1
}

func main() {
	fmt.Println(shortestSubarraySumK([]int{2, -1, 2}, 3))
}
