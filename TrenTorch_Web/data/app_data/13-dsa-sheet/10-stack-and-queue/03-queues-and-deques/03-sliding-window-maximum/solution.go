package main

import "fmt"

// O(n) time, O(k) space for the window (plus O(n - k + 1) for the output)
func slidingWindowMax(nums []int, k int) []int {
	window := []int{}
	head := 0
	out := []int{}
	for i, x := range nums {
		for len(window) > head && nums[window[len(window)-1]] <= x {
			window = window[:len(window)-1]
		}
		window = append(window, i)
		if window[head] <= i-k {
			head++
		}
		if i >= k-1 {
			out = append(out, nums[window[head]])
		}
	}
	return out
}

func main() {
	fmt.Println(slidingWindowMax([]int{1, 3, -1, -3, 5, 3, 6, 7}, 3))
}
