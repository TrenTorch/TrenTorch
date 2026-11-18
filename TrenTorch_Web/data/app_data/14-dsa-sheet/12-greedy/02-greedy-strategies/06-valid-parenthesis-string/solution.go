package main

import "fmt"

// O(n) time, O(1) space
func checkValidString(s string) bool {
	lo, hi := 0, 0
	for i := 0; i < len(s); i++ {
		switch s[i] {
		case '(':
			lo++
			hi++
		case ')':
			lo--
			hi--
		default:
			lo--
			hi++
		}
		if hi < 0 {
			return false
		}
		if lo < 0 {
			lo = 0
		}
	}
	return lo == 0
}

func main() {
	fmt.Println(checkValidString("(*)"))
}
