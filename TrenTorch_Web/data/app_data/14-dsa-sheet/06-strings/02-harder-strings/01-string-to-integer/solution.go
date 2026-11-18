package main

import "fmt"

// O(n) time, O(1) space
func myAtoi(s string) int {
	i, n := 0, len(s)
	for i < n && s[i] == ' ' {
		i++
	}
	sign := 1
	if i < n && (s[i] == '+' || s[i] == '-') {
		if s[i] == '-' {
			sign = -1
		}
		i++
	}
	value := 0
	for i < n && s[i] >= '0' && s[i] <= '9' {
		value = value*10 + int(s[i]-'0')
		i++
		if value > 1<<31 {
			break
		}
	}
	value *= sign
	if value < -(1 << 31) {
		return -(1 << 31)
	}
	if value > 1<<31-1 {
		return 1<<31 - 1
	}
	return value
}

func main() {
	fmt.Println(myAtoi("42"))
}
