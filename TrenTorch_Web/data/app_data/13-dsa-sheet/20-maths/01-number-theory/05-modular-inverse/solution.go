package main

import "fmt"

// O(log m) time, O(1) space
func modInverse(a int, m int) int {
	if m == 1 {
		return 0
	}
	oldR, r := a%m, m
	oldX, x := 1, 0
	for r != 0 {
		q := oldR / r
		oldR, r = r, oldR-q*r
		oldX, x = x, oldX-q*x
	}
	if oldR == 1 {
		return ((oldX % m) + m) % m
	}
	return -1
}

func main() {
	fmt.Println(modInverse(3, 11))
}
