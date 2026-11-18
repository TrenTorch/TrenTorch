package main

import "fmt"

// O(1) time, O(1) space
func fewestNotes(amount int) int {
	total := 0
	for _, value := range [...]int{2000, 500, 100, 50, 20, 10, 5, 2, 1} {
		count := amount / value
		amount %= value
		total += count
	}
	return total
}

func main() {
	fmt.Println(fewestNotes(70))
}
