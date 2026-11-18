package main

import "fmt"

// O(n) time, O(1) space
func singleNumberIi(nums []int) int {
	ones, twos := 0, 0
	for _, x := range nums {
		ones = (ones ^ x) &^ twos
		twos = (twos ^ x) &^ ones
	}
	return ones
}

func main() {
	fmt.Println(singleNumberIi([]int{2, 2, 3, 2}))
}
