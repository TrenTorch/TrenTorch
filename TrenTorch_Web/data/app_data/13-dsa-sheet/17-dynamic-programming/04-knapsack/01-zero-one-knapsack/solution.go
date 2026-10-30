package main

import "fmt"

// O(n * capacity) time, O(capacity) space
func knapsack(weights []int, values []int, capacity int) int {
	best := make([]int, capacity+1)
	for i := 0; i < len(weights) && i < len(values); i++ {
		weight, value := weights[i], values[i]
		for w := capacity; w >= weight; w-- {
			if best[w-weight]+value > best[w] {
				best[w] = best[w-weight] + value
			}
		}
	}
	return best[capacity]
}

func main() {
	fmt.Println(knapsack([]int{1, 3, 4, 5}, []int{1, 4, 5, 7}, 7))
}
