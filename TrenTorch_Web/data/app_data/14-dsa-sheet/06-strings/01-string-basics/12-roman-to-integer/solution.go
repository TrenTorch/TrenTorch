package main

import "fmt"

// O(n) time, O(1) space
func romanToInteger(s string) int {
	values := map[byte]int{'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
	total := 0
	for i := 0; i < len(s); i++ {
		v := values[s[i]]
		if i+1 < len(s) && v < values[s[i+1]] {
			total -= v
		} else {
			total += v
		}
	}
	return total
}

func main() {
	fmt.Println(romanToInteger("III"))
}
