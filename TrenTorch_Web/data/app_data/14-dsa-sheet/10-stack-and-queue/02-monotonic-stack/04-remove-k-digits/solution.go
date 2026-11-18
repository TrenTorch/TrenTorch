package main

import (
	"fmt"
	"strings"
)

// O(n) time, O(n) space
func removeKDigits(num string, k int) string {
	stack := []byte{}
	for i := 0; i < len(num); i++ {
		ch := num[i]
		for k > 0 && len(stack) > 0 && stack[len(stack)-1] > ch {
			stack = stack[:len(stack)-1]
			k--
		}
		stack = append(stack, ch)
	}
	if k > 0 {
		stack = stack[:len(stack)-k]
	}
	res := strings.TrimLeft(string(stack), "0")
	if res == "" {
		return "0"
	}
	return res
}

func main() {
	fmt.Println(removeKDigits("1432219", 3))
}
