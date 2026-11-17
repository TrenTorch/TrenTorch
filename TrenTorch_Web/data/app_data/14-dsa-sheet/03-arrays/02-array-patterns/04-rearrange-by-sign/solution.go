package main

import "fmt"

// O(n) time, O(n) space
func rearrangeBySign(nums []int) []int {
	pos := []int{}
	neg := []int{}
	for _, x := range nums {
		if x >= 0 {
			pos = append(pos, x)
		} else {
			neg = append(neg, x)
		}
	}
	out := make([]int, 0, len(nums))
	for i := 0; i < max(len(pos), len(neg)); i++ {
		if i < len(pos) {
			out = append(out, pos[i])
		}
		if i < len(neg) {
			out = append(out, neg[i])
		}
	}
	return out
}

func main() {
	fmt.Println(rearrangeBySign([]int{3, 1, -2, -5, 2, -4}))
}
