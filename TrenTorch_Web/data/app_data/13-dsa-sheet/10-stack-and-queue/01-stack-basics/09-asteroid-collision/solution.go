package main

import "fmt"

// O(n) time, O(n) space
func asteroidCollision(asteroids []int) []int {
	stack := []int{}
	for _, a := range asteroids {
		alive := true
		for alive && a < 0 && len(stack) > 0 && stack[len(stack)-1] > 0 {
			top := stack[len(stack)-1]
			if top < -a {
				stack = stack[:len(stack)-1]
			} else if top == -a {
				stack = stack[:len(stack)-1]
				alive = false
			} else {
				alive = false
			}
		}
		if alive {
			stack = append(stack, a)
		}
	}
	return stack
}

func main() {
	fmt.Println(asteroidCollision([]int{5, 10, -5}))
}
