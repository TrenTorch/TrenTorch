package main

import "fmt"

type frame struct {
	result int
	sign   int
}

// O(n) time, O(n) space (stack depth = bracket nesting)
func calculateBrackets(s string) int {
	stack := []frame{}
	result := 0
	num := 0
	sign := 1
	for i := 0; i < len(s); i++ {
		ch := s[i]
		if ch >= '0' && ch <= '9' {
			num = num*10 + int(ch-'0')
		} else if ch == '+' || ch == '-' {
			result += sign * num
			num = 0
			if ch == '+' {
				sign = 1
			} else {
				sign = -1
			}
		} else if ch == '(' {
			stack = append(stack, frame{result: result, sign: sign})
			result, sign = 0, 1
		} else if ch == ')' {
			result += sign * num
			num = 0
			saved := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			result = saved.result + saved.sign*result
		}
	}
	return result + sign*num
}

func main() {
	fmt.Println(calculateBrackets("(1+(4+5+2)-3)+(6+8)"))
}
