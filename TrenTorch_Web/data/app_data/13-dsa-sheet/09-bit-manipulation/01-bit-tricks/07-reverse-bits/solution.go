package main

import "fmt"

// O(1) time (32 iterations), O(1) space
func reverseBits(n int) int {
	result := 0
	for i := 0; i < 32; i++ {
		result = (result << 1) | (n & 1)
		n >>= 1
	}
	return result
}

func main() {
	fmt.Println(reverseBits(1))
}
