package main

import "fmt"

func absInt(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

// O(n) time, O(1) space
func calculate(s string) int {
	total, last, num := 0, 0, 0
	op := byte('+')
	expr := s + "+"
	for i := 0; i < len(expr); i++ {
		ch := expr[i]
		if ch >= '0' && ch <= '9' {
			num = num*10 + int(ch-'0')
		} else if ch != ' ' {
			switch op {
			case '+':
				total += last
				last = num
			case '-':
				total += last
				last = -num
			case '*':
				last *= num
			default:
				q := absInt(last) / num
				if last >= 0 {
					last = q
				} else {
					last = -q
				}
			}
			op = ch
			num = 0
		}
	}
	return total + last
}

func main() {
	fmt.Println(calculate("3+2*2"))
}
