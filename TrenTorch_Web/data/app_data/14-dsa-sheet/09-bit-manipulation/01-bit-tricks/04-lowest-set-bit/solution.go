package main

import "fmt"

// O(1) time, O(1) space
func lowestSetBit(n int) int {
	return n & -n
}

func main() {
	fmt.Println(lowestSetBit(12))
}
