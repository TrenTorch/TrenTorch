package main

import "fmt"

// O(n) time, O(1) space
func longestMountain(arr []int) int {
	n := len(arr)
	best := 0
	i := 1
	for i < n-1 {
		if arr[i-1] < arr[i] && arr[i] > arr[i+1] {
			left := i - 1
			for left > 0 && arr[left-1] < arr[left] {
				left--
			}
			right := i + 1
			for right < n-1 && arr[right] > arr[right+1] {
				right++
			}
			if right-left+1 > best {
				best = right - left + 1
			}
			i = right + 1
		} else {
			i++
		}
	}
	return best
}

func main() {
	fmt.Println(longestMountain([]int{2, 1, 4, 7, 3, 2, 5}))
}
