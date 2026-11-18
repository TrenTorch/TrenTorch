package main

import "fmt"

// O(1) time (31 bit positions), O(1) space
func minFlips(a int, b int, c int) int {
	flips := 0
	for i := 0; i < 31; i++ {
		x := (a >> i) & 1
		y := (b >> i) & 1
		z := (c >> i) & 1
		if z == 0 {
			flips += x + y
		} else if x == 0 && y == 0 {
			flips++
		}
	}
	return flips
}

func main() {
	fmt.Println(minFlips(2, 6, 5))
}
