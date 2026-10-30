package main

import "fmt"

// O(n) time, O(n) space (keep non-zero values in order, then append the zeros).
func moveZeros(nums []int) []int {
	out := make([]int, 0, len(nums))
	zeros := 0
	for _, x := range nums {
		if x == 0 {
			zeros++
		} else {
			out = append(out, x)
		}
	}
	for i := 0; i < zeros; i++ {
		out = append(out, 0)
	}
	return out
}

func main() {
	fmt.Println(moveZeros([]int{0, 1, 0, 3, 12}))
}
