package main

import "fmt"

// O(n) time, O(1) space
func canJump(nums []int) bool {
	far := 0
	for i, jump := range nums {
		if i > far {
			return false
		}
		if i+jump > far {
			far = i + jump
		}
	}
	return true
}

func main() {
	fmt.Println(canJump([]int{2, 3, 1, 1, 4}))
}
