package main

import "fmt"

// O(n) time, O(n) space
func nextPermutation(nums []int) []int {
	a := make([]int, len(nums))
	copy(a, nums)
	i := len(a) - 2
	for i >= 0 && a[i] >= a[i+1] {
		i--
	}
	if i >= 0 {
		j := len(a) - 1
		for a[j] <= a[i] {
			j--
		}
		a[i], a[j] = a[j], a[i]
	}
	for l, r := i+1, len(a)-1; l < r; l, r = l+1, r-1 {
		a[l], a[r] = a[r], a[l]
	}
	return a
}

func main() {
	fmt.Println(nextPermutation([]int{1, 2, 3}))
}
