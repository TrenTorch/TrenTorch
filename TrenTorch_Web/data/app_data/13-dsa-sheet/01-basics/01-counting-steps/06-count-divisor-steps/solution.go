package main

import "fmt"

// O(sqrt(n)) time, O(1) space
func countDivisorSteps(n int) int {
	total := 0
	i := 1
	for i <= n {
		q := n / i
		j := n / q
		total += q * (j - i + 1)
		i = j + 1
	}
	return total
}

func main() {
	fmt.Println(countDivisorSteps(5))
}
