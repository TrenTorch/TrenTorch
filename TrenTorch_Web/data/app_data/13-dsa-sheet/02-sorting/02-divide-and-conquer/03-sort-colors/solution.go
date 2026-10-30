package main

import "fmt"

// O(n) time, O(n) space (count each color, then write them back in order).
func sortColors(nums []int) []int {
	var count [3]int
	for _, v := range nums {
		count[v]++
	}
	out := make([]int, 0, len(nums))
	for v := 0; v < 3; v++ {
		for k := 0; k < count[v]; k++ {
			out = append(out, v)
		}
	}
	return out
}

func main() {
	fmt.Println(sortColors([]int{2, 0, 2, 1, 1, 0}))
}
