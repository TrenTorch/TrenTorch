package main

import "fmt"

// O(n) time, O(1) space
func longestValidParentheses(s string) int {
	best := 0
	n := len(s)
	for pass := 0; pass < 2; pass++ {
		opener := byte('(')
		if pass == 1 {
			opener = ')'
		}
		left, right := 0, 0
		for k := 0; k < n; k++ {
			idx := k
			if pass == 1 {
				idx = n - 1 - k
			}
			if s[idx] == opener {
				left++
			} else {
				right++
			}
			if left == right {
				best = max(best, 2*left)
			} else if right > left {
				left, right = 0, 0
			}
		}
	}
	return best
}

func main() {
	fmt.Println(longestValidParentheses(")()())"))
}
