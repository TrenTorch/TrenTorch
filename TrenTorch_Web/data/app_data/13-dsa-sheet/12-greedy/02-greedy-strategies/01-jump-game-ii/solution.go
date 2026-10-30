package main

import "fmt"

// O(n) time, O(1) space
func minJumps(nums []int) int {
	n := len(nums)
	if n <= 1 {
		return 0
	}
	jumps, end, far := 0, 0, 0
	for i := 0; i < n-1; i++ {
		if i+nums[i] > far {
			far = i + nums[i]
		}
		if i == far {
			return -1
		}
		if i == end {
			jumps++
			end = far
			if end >= n-1 {
				break
			}
		}
	}
	if end >= n-1 {
		return jumps
	}
	return -1
}

func main() {
	fmt.Println(minJumps([]int{2, 3, 1, 1, 4}))
}
