package main

import "fmt"

// O(1) time, O(1) space
func countPairs(n int) int {
	return n * (n - 1) / 2
}

func main() {
	fmt.Println(countPairs(4))
}
