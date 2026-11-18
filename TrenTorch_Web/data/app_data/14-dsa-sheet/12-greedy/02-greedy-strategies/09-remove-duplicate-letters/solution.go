package main

import "fmt"

// O(n) time, O(1) space (fixed 256-entry tables)
func removeDuplicateLetters(s string) string {
	var last [256]int
	for i := 0; i < len(s); i++ {
		last[s[i]] = i
	}
	var inStack [256]bool
	stack := make([]byte, 0, len(s))
	for i := 0; i < len(s); i++ {
		ch := s[i]
		if inStack[ch] {
			continue
		}
		for len(stack) > 0 && stack[len(stack)-1] > ch && last[stack[len(stack)-1]] > i {
			inStack[stack[len(stack)-1]] = false
			stack = stack[:len(stack)-1]
		}
		stack = append(stack, ch)
		inStack[ch] = true
	}
	return string(stack)
}

func main() {
	fmt.Println(removeDuplicateLetters("bcabc"))
}
