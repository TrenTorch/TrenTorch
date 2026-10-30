package main

import "fmt"

// O(n) time, O(1) space
func validPalindromeIi(s string) bool {
	isPal := func(i, j int) bool {
		for i < j {
			if s[i] != s[j] {
				return false
			}
			i++
			j--
		}
		return true
	}
	i, j := 0, len(s)-1
	for i < j {
		if s[i] != s[j] {
			return isPal(i+1, j) || isPal(i, j-1)
		}
		i++
		j--
	}
	return true
}

func main() {
	fmt.Println(validPalindromeIi("aba"))
}
