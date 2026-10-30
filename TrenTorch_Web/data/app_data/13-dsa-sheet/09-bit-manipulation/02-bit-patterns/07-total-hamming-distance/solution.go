package main

import "fmt"

// O(30 n) time, O(1) space
func totalHammingDistance(nums []int) int {
	n := len(nums)
	total := 0
	for i := 0; i < 30; i++ {
		ones := 0
		for _, x := range nums {
			ones += (x >> i) & 1
		}
		total += ones * (n - ones)
	}
	return total
}

func main() {
	fmt.Println(totalHammingDistance([]int{4, 14, 2}))
}
