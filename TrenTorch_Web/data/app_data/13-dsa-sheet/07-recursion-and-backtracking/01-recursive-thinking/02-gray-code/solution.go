package main

import "fmt"

// O(2^n) time, O(2^n) space
func grayCode(n int) []int {
	out := make([]int, 1<<n)
	for i := range out {
		out[i] = i ^ (i >> 1)
	}
	return out
}

func main() {
	fmt.Println(grayCode(2))
}
