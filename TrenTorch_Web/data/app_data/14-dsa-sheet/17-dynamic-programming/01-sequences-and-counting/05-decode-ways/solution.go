package main

import "fmt"

// O(n) time, O(1) space
func numDecodings(s string) int {
	const mod = 1000000007
	if len(s) == 0 {
		return 0
	}
	a, b := 1, 1
	for i := 1; i <= len(s); i++ {
		now := 0
		if s[i-1] != '0' {
			now += b
		}
		if i >= 2 {
			two := s[i-2 : i]
			if two >= "10" && two <= "26" {
				now += a
			}
		}
		a, b = b, now%mod
	}
	return b % mod
}

func main() {
	fmt.Println(numDecodings("12"))
}
