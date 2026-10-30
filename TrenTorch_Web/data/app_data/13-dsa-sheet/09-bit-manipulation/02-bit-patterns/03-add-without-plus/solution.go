package main

import "fmt"

// O(1) time (at most 32 carry rounds), O(1) space
func bitAdd(a int, b int) int {
	mask := 0xFFFFFFFF
	a &= mask
	b &= mask
	for b != 0 {
		a, b = (a^b)&mask, ((a&b)<<1)&mask
	}
	if a >= 1<<31 {
		return a - (1 << 32)
	}
	return a
}

func main() {
	fmt.Println(bitAdd(1, 2))
}
