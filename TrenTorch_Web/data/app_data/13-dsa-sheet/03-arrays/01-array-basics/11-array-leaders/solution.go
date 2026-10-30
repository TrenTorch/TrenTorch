package main

import "fmt"

// O(n) time, O(n) space
func arrayLeaders(nums []int) []int {
	out := []int{}
	found := false
	best := 0
	for i := len(nums) - 1; i >= 0; i-- {
		x := nums[i]
		if !found || x > best {
			out = append(out, x)
			best = x
			found = true
		}
	}
	for l, r := 0, len(out)-1; l < r; l, r = l+1, r-1 {
		out[l], out[r] = out[r], out[l]
	}
	return out
}

func main() {
	fmt.Println(arrayLeaders([]int{16, 17, 4, 3, 5, 2}))
}
