package main

import "fmt"

// O(n) time, O(n) space
func removeOuterParentheses(s string) string {
	out := make([]byte, 0, len(s))
	depth := 0
	for i := 0; i < len(s); i++ {
		ch := s[i]
		if ch == '(' {
			if depth > 0 {
				out = append(out, ch)
			}
			depth++
		} else {
			depth--
			if depth > 0 {
				out = append(out, ch)
			}
		}
	}
	return string(out)
}

func main() {
	fmt.Println(removeOuterParentheses("(()())(())"))
}
