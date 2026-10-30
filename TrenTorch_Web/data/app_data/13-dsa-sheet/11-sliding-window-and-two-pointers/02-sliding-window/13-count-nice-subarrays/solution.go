package main

import "fmt"

// O(n) time, O(1) space
func numberOfSubarrays(nums []int, k int) int {
	atMost := func(m int) int {
		if m < 0 {
			return 0
		}
		odd := 0
		left := 0
		total := 0
		for right, x := range nums {
			odd += x % 2
			for odd > m {
				odd -= nums[left] % 2
				left++
			}
			total += right - left + 1
		}
		return total
	}
	return atMost(k) - atMost(k-1)
}

func main() {
	fmt.Println(numberOfSubarrays([]int{1, 1, 2, 1, 1}, 3))
}
