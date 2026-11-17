package main

import "fmt"

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// O(n * log(M)) time, O(1) space, where M is the largest value (int arithmetic; overflows for large results).
func lcmOfList(nums []int) int {
	result := 1
	for _, x := range nums {
		result = result / gcd(result, x) * x
	}
	return result
}

func main() {
	fmt.Println(lcmOfList([]int{4, 6, 10}))
}
