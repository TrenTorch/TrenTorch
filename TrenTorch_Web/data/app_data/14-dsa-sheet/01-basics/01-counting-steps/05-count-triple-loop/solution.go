package main

import "fmt"

// O(1) time, O(1) space
func countTripleLoop(n int) int {
	return n * (n + 1) * (n + 2) / 6
}

func main() {
	fmt.Println(countTripleLoop(3))
}
