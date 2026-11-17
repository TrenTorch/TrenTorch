package main

import "fmt"

// O(n) time, O(1) space
func gasStation(gas []int, cost []int) int {
	total, tank, start := 0, 0, 0
	for i := range gas {
		diff := gas[i] - cost[i]
		total += diff
		tank += diff
		if tank < 0 {
			start = i + 1
			tank = 0
		}
	}
	if total >= 0 && len(gas) > 0 {
		return start
	}
	return -1
}

func main() {
	fmt.Println(gasStation([]int{1, 2, 3, 4, 5}, []int{3, 4, 5, 1, 2}))
}
