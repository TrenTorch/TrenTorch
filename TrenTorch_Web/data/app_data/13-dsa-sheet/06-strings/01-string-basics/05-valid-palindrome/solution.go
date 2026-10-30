package main

import "fmt"

func isAlnum(c byte) bool {
	return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9')
}

func toLowerByte(c byte) byte {
	if c >= 'A' && c <= 'Z' {
		return c + ('a' - 'A')
	}
	return c
}

// O(n) time, O(1) space
func validPalindrome(s string) bool {
	i, j := 0, len(s)-1
	for i < j {
		if !isAlnum(s[i]) {
			i++
		} else if !isAlnum(s[j]) {
			j--
		} else {
			if toLowerByte(s[i]) != toLowerByte(s[j]) {
				return false
			}
			i++
			j--
		}
	}
	return true
}

func main() {
	fmt.Println(validPalindrome("A man, a plan, a canal: Panama"))
}
