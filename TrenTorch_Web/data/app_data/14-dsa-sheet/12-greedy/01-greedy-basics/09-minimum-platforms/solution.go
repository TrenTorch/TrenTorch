package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space
func minPlatforms(arrivals []int, departures []int) int {
	arr := append([]int(nil), arrivals...)
	dep := append([]int(nil), departures...)
	sort.Ints(arr)
	sort.Ints(dep)
	current, best := 0, 0
	i, j := 0, 0
	for i < len(arr) {
		if arr[i] <= dep[j] {
			current++
			if current > best {
				best = current
			}
			i++
		} else {
			current--
			j++
		}
	}
	return best
}

func main() {
	fmt.Println(minPlatforms([]int{900, 940, 950, 1100, 1500, 1800}, []int{910, 1200, 1120, 1130, 1900, 2000}))
}
