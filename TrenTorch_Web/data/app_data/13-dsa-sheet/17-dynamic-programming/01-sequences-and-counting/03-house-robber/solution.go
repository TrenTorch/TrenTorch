package main

import "fmt"

// O(n) time, O(1) space
func rob(nums []int) int {
	skip, take := 0, 0
	for _, x := range nums {
		skip, take = max(skip, take), skip+x
	}
	return max(skip, take)
}

func main() {
	fmt.Println(rob([]int{1, 2, 3, 1}))
}
