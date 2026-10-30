package main

import (
	"fmt"
	"strconv"
)

// O(n) time, O(n) space
func evaluateRpn(tokens []string) int {
	stack := []int{}
	for _, token := range tokens {
		switch token {
		case "+", "-", "*", "/":
			b := stack[len(stack)-1]
			a := stack[len(stack)-2]
			stack = stack[:len(stack)-2]
			switch token {
			case "+":
				stack = append(stack, a+b)
			case "-":
				stack = append(stack, a-b)
			case "*":
				stack = append(stack, a*b)
			default:
				q := absInt(a) / absInt(b)
				if (a < 0) == (b < 0) {
					stack = append(stack, q)
				} else {
					stack = append(stack, -q)
				}
			}
		default:
			v, err := strconv.Atoi(token)
			if err != nil {
				panic(fmt.Sprintf("invalid token %q: %v", token, err))
			}
			stack = append(stack, v)
		}
	}
	return stack[0]
}

func absInt(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	fmt.Println(evaluateRpn([]string{"2", "1", "+", "3", "*"}))
}
