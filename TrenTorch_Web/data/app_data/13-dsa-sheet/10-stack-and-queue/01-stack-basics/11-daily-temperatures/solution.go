package main

import "fmt"

// O(n) time, O(n) space
func dailyTemperatures(temps []int) []int {
	out := make([]int, len(temps))
	stack := []int{}
	for i, t := range temps {
		for len(stack) > 0 && temps[stack[len(stack)-1]] < t {
			j := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			out[j] = i - j
		}
		stack = append(stack, i)
	}
	return out
}

func main() {
	fmt.Println(dailyTemperatures([]int{73, 74, 75, 71, 69, 72, 76, 73}))
}
