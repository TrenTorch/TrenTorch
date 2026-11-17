package main

import "fmt"

// prefixXor returns 0 ^ 1 ^ ... ^ n in O(1) time and O(1) space.
func prefixXor(n int) int {
	if n < 0 {
		return 0
	}
	switch n % 4 {
	case 0:
		return n
	case 1:
		return 1
	case 2:
		return n + 1
	}
	return 0
}

// O(1) time, O(1) space
func xorOfRange(left int, right int) int {
	return prefixXor(right) ^ prefixXor(left-1)
}

func main() {
	fmt.Println(xorOfRange(3, 9))
}
