package main

import "fmt"

// O(k) time where k is the number of differing bits, O(1) space
func bitFlipsToConvert(a int, b int) int {
	diff := a ^ b
	count := 0
	for diff != 0 {
		diff &= diff - 1
		count++
	}
	return count
}

func main() {
	fmt.Println(bitFlipsToConvert(10, 7))
}
