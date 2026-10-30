package main

import "fmt"

// O(n * capacity) time, O(capacity) space
func unboundedKnapsack(weights []int, values []int, capacity int) int {
	best := make([]int, capacity+1)
	for i := 0; i < len(weights) && i < len(values); i++ {
		weight, value := weights[i], values[i]
		for w := weight; w <= capacity; w++ {
			if best[w-weight]+value > best[w] {
				best[w] = best[w-weight] + value
			}
		}
	}
	return best[capacity]
}

func main() {
	fmt.Println(unboundedKnapsack([]int{1, 3, 4}, []int{15, 50, 60}, 8))
}
