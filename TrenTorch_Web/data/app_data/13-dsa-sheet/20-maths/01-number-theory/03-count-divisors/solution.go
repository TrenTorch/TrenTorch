package main

import "fmt"

// O(sqrt(n)) time, O(1) space
func countDivisors(n int) int {
	count := 0
	for d := 1; d*d <= n; d++ {
		if n%d == 0 {
			if d*d == n {
				count++
			} else {
				count += 2
			}
		}
	}
	return count
}

func main() {
	fmt.Println(countDivisors(36))
}
