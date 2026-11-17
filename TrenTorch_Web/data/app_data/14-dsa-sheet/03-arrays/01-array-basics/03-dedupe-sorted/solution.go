package main

import "fmt"

// O(n) time, O(n) space for the output (compare each value with the last one kept).
func dedupeSorted(nums []int) []int {
	out := make([]int, 0, len(nums))
	for _, x := range nums {
		if len(out) == 0 || out[len(out)-1] != x {
			out = append(out, x)
		}
	}
	return out
}

func main() {
	fmt.Println(dedupeSorted([]int{1, 1, 2, 2, 2, 3}))
}
