package main

import "fmt"

// O(n) time, O(n) space
func removeAdjacentDuplicates(s string) string {
	stack := make([]byte, 0, len(s))
	for i := 0; i < len(s); i++ {
		ch := s[i]
		if len(stack) > 0 && stack[len(stack)-1] == ch {
			stack = stack[:len(stack)-1]
		} else {
			stack = append(stack, ch)
		}
	}
	return string(stack)
}

func main() {
	fmt.Println(removeAdjacentDuplicates("abbaca"))
}
