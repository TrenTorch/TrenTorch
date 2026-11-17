package main

import "fmt"

// O(1) time, O(1) space
func isPowerOfTwo(n int) bool {
	return n > 0 && (n&(n-1)) == 0
}

func main() {
	fmt.Println(isPowerOfTwo(16))
}
