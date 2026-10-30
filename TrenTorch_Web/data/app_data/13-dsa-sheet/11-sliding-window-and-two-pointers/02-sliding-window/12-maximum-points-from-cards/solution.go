package main

import "fmt"

// O(n) time, O(1) space
func maxPoints(points []int, k int) int {
	n := len(points)
	size := n - k
	window := 0
	for i := 0; i < size; i++ {
		window += points[i]
	}
	smallest := window
	for i := size; i < n; i++ {
		window += points[i] - points[i-size]
		if window < smallest {
			smallest = window
		}
	}
	total := 0
	for _, p := range points {
		total += p
	}
	return total - smallest
}

func main() {
	fmt.Println(maxPoints([]int{1, 2, 3, 4, 5, 6, 1}, 3))
}
