package main

import "fmt"

// O(n) time, O(n) space
func sumSubarrayMins(arr []int) int {
	const mod = 1000000007
	n := len(arr)
	left := make([]int, n)
	right := make([]int, n)
	stack := []int{}
	for i := 0; i < n; i++ {
		for len(stack) > 0 && arr[stack[len(stack)-1]] >= arr[i] {
			stack = stack[:len(stack)-1]
		}
		if len(stack) > 0 {
			left[i] = stack[len(stack)-1]
		} else {
			left[i] = -1
		}
		stack = append(stack, i)
	}
	stack = stack[:0]
	for i := n - 1; i >= 0; i-- {
		for len(stack) > 0 && arr[stack[len(stack)-1]] > arr[i] {
			stack = stack[:len(stack)-1]
		}
		if len(stack) > 0 {
			right[i] = stack[len(stack)-1]
		} else {
			right[i] = n
		}
		stack = append(stack, i)
	}
	total := 0
	for i := 0; i < n; i++ {
		total = (total + arr[i]*(i-left[i])*(right[i]-i)) % mod
	}
	return total
}

func main() {
	fmt.Println(sumSubarrayMins([]int{3, 1, 2, 4}))
}
