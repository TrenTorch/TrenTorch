package main

import "fmt"

// O(n) time, O(1) space
func robCircle(nums []int) int {
	if len(nums) == 0 {
		return 0
	}
	if len(nums) == 1 {
		return nums[0]
	}
	line := func(houses []int) int {
		skip, take := 0, 0
		for _, x := range houses {
			skip, take = max(skip, take), skip+x
		}
		return max(skip, take)
	}
	return max(line(nums[1:]), line(nums[:len(nums)-1]))
}

func main() {
	fmt.Println(robCircle([]int{2, 3, 2}))
}
