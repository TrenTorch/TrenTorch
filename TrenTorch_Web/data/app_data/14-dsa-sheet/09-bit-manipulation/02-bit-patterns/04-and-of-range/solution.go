package main

import "fmt"

// O(log m) time, O(1) space, where m is the bit length of right
func andOfRange(left int, right int) int {
	shift := 0
	for x := left ^ right; x > 0; x >>= 1 {
		shift++
	}
	return (left >> shift) << shift
}

func main() {
	fmt.Println(andOfRange(5, 7))
}
