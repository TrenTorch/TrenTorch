package main

import "fmt"

// O(n) time, O(1) space
func josephus(n int, k int) int {
	position := 0
	for m := 2; m <= n; m++ {
		position = (position + k) % m
	}
	return position + 1
}

func main() {
	fmt.Println(josephus(5, 2))
}
