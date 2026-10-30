package main

import "fmt"

// O(4^n / sqrt(n)) time (Catalan count of outputs, length 2n each), O(n) extra space
func generateParentheses(n int) []string {
	out := []string{}
	buf := make([]byte, 0, 2*n)
	var rec func(opens, closes int)
	rec = func(opens, closes int) {
		if len(buf) == 2*n {
			out = append(out, string(buf))
			return
		}
		if opens < n {
			buf = append(buf, '(')
			rec(opens+1, closes)
			buf = buf[:len(buf)-1]
		}
		if closes < opens {
			buf = append(buf, ')')
			rec(opens, closes+1)
			buf = buf[:len(buf)-1]
		}
	}
	rec(0, 0)
	return out
}

func main() {
	fmt.Println(generateParentheses(3))
}
