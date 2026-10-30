package main

import "fmt"

// O(n) time, O(n) space
func countBitsUpTo(n int) []int {
	bits := make([]int, n+1)
	for i := 1; i <= n; i++ {
		bits[i] = bits[i>>1] + (i & 1)
	}
	return bits
}

func main() {
	fmt.Println(countBitsUpTo(5))
}
