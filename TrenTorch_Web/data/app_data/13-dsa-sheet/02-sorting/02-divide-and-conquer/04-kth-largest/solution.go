package main

import (
	"fmt"
	"math/rand"
)

// O(n) expected time, O(n) space (randomized quickselect on a copy of the input).
func kthLargest(nums []int, k int) int {
	a := append([]int(nil), nums...)
	target := len(a) - k
	for {
		pivot := a[rand.Intn(len(a))]
		less := []int{}
		greater := []int{}
		equal := 0
		for _, x := range a {
			if x < pivot {
				less = append(less, x)
			} else if x == pivot {
				equal++
			} else {
				greater = append(greater, x)
			}
		}
		if target < len(less) {
			a = less
		} else if target < len(less)+equal {
			return pivot
		} else {
			target -= len(less) + equal
			a = greater
		}
	}
}

func main() {
	fmt.Println(kthLargest([]int{3, 2, 1, 5, 6, 4}, 2))
}
