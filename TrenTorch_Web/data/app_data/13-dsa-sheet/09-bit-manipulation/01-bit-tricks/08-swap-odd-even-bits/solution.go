package main

import "fmt"

// O(1) time, O(1) space
func swapOddEvenBits(n int) int {
	return ((n & 0x55555555) << 1) | ((n & 0xAAAAAAAA) >> 1)
}

func main() {
	fmt.Println(swapOddEvenBits(10))
}
