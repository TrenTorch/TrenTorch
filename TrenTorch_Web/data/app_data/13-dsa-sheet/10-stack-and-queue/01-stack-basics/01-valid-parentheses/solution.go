package main

import "fmt"

// O(n) time, O(n) space
func validBrackets(s string) bool {
	match := map[byte]byte{')': '(', ']': '[', '}': '{'}
	stack := []byte{}
	for i := 0; i < len(s); i++ {
		ch := s[i]
		if open, ok := match[ch]; ok {
			if len(stack) == 0 || stack[len(stack)-1] != open {
				return false
			}
			stack = stack[:len(stack)-1]
		} else {
			stack = append(stack, ch)
		}
	}
	return len(stack) == 0
}

func main() {
	fmt.Println(validBrackets("()[]{}"))
}
