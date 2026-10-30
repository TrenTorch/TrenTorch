package main

import "fmt"

// O(n) time, O(n) space
func longestWithinLimit(nums []int, limit int) int {
	big := []int{}
	small := []int{}
	bigHead, smallHead := 0, 0
	left := 0
	best := 0
	for right, x := range nums {
		for len(big) > bigHead && nums[big[len(big)-1]] <= x {
			big = big[:len(big)-1]
		}
		big = append(big, right)
		for len(small) > smallHead && nums[small[len(small)-1]] >= x {
			small = small[:len(small)-1]
		}
		small = append(small, right)
		for nums[big[bigHead]]-nums[small[smallHead]] > limit {
			left++
			if big[bigHead] < left {
				bigHead++
			}
			if small[smallHead] < left {
				smallHead++
			}
		}
		best = max(best, right-left+1)
	}
	return best
}

func main() {
	fmt.Println(longestWithinLimit([]int{8, 2, 4, 7}, 4))
}
