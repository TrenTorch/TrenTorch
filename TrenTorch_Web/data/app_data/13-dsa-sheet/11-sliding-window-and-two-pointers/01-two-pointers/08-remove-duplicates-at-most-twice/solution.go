package main

import "fmt"

// O(n) time, O(n) space
func keepAtMostTwice(nums []int) []int {
	a := make([]int, len(nums))
	copy(a, nums)
	write := 0
	for read := 0; read < len(a); read++ {
		if write < 2 || a[read] != a[write-2] {
			a[write] = a[read]
			write++
		}
	}
	return a[:write]
}

func main() {
	fmt.Println(keepAtMostTwice([]int{1, 1, 1, 2, 2, 3}))
}
