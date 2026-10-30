package main

import "fmt"

// O(n) time, O(n) space (map of at most k+1 distinct values)
func subarraysKDistinct(nums []int, k int) int {
	atMost := func(m int) int {
		count := make(map[int]int)
		left := 0
		total := 0
		for right, x := range nums {
			count[x]++
			for len(count) > m {
				count[nums[left]]--
				if count[nums[left]] == 0 {
					delete(count, nums[left])
				}
				left++
			}
			total += right - left + 1
		}
		return total
	}
	return atMost(k) - atMost(k-1)
}

func main() {
	fmt.Println(subarraysKDistinct([]int{1, 2, 1, 2, 3}, 2))
}
