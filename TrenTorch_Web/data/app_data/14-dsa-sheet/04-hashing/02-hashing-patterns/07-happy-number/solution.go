package main

import "fmt"

// O(log n) time, O(1) space
func happyNumber(n int) bool {
	step := func(x int) int {
		total := 0
		for x != 0 {
			digit := x % 10
			x /= 10
			total += digit * digit
		}
		return total
	}

	slow, fast := n, step(n)
	for fast != 1 && slow != fast {
		slow = step(slow)
		fast = step(step(fast))
	}
	return fast == 1
}

func main() {
	fmt.Println(happyNumber(19))
}
