package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space
func carFleet(target int, cars [][]int) int {
	sorted := make([][]int, len(cars))
	copy(sorted, cars)
	sort.Slice(sorted, func(a, b int) bool {
		return sorted[a][0] > sorted[b][0]
	})
	fleets := 0
	slowNum, slowDen := 0, 1
	for _, c := range sorted {
		num, den := target-c[0], c[1]
		if num*slowDen > slowNum*den {
			fleets++
			slowNum, slowDen = num, den
		}
	}
	return fleets
}

func main() {
	fmt.Println(carFleet(12, [][]int{[]int{10, 2}, []int{8, 4}, []int{0, 1}, []int{5, 1}, []int{3, 3}}))
}
