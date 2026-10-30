package main

import "fmt"

// O(1) time, O(1) space
func isPowerOfFour(n int) bool {
	return n > 0 && (n&(n-1)) == 0 && (n&0x5555555555555555) != 0
}

func main() {
	fmt.Println(isPowerOfFour(16))
}
