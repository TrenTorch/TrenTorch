package main

import "fmt"

// O(log_5 n) time, O(1) space
func trailingZeros(n int) int {
	count := 0
	for n > 0 {
		n /= 5
		count += n
	}
	return count
}

func main() {
	fmt.Println(trailingZeros(25))
}
