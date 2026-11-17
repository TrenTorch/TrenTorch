package main

import "fmt"

// O(k) time where k is the number of set bits, O(1) space
func countSetBits(n int) int {
	count := 0
	for n != 0 {
		n &= n - 1
		count++
	}
	return count
}

func main() {
	fmt.Println(countSetBits(13))
}
