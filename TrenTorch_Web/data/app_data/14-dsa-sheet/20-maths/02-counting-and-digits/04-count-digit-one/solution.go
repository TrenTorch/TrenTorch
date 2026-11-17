package main

import "fmt"

// O(log n) time, O(1) space
func countDigitOne(n int) int {
	total := 0
	for p := 1; p <= n; p *= 10 {
		high := n / (p * 10)
		cur := (n / p) % 10
		low := n % p
		total += high * p
		if cur > 1 {
			total += p
		} else if cur == 1 {
			total += low + 1
		}
	}
	return total
}

func main() {
	fmt.Println(countDigitOne(13))
}
