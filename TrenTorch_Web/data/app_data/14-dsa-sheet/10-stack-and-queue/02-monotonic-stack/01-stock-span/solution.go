package main

import "fmt"

// O(n) time, O(n) space
func stockSpan(prices []int) []int {
	out := make([]int, 0, len(prices))
	stack := []int{}
	for i, p := range prices {
		for len(stack) > 0 && prices[stack[len(stack)-1]] <= p {
			stack = stack[:len(stack)-1]
		}
		if len(stack) > 0 {
			out = append(out, i-stack[len(stack)-1])
		} else {
			out = append(out, i+1)
		}
		stack = append(stack, i)
	}
	return out
}

func main() {
	fmt.Println(stockSpan([]int{100, 80, 60, 70, 60, 75, 85}))
}
