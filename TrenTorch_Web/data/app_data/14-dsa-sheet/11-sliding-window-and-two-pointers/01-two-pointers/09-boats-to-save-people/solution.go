package main

import (
	"fmt"
	"sort"
)

// O(n log n) time, O(n) space
func boatsNeeded(people []int, limit int) int {
	a := make([]int, len(people))
	copy(a, people)
	sort.Ints(a)
	light, heavy := 0, len(a)-1
	boats := 0
	for light <= heavy {
		if a[light]+a[heavy] <= limit {
			light++
		}
		heavy--
		boats++
	}
	return boats
}

func main() {
	fmt.Println(boatsNeeded([]int{3, 2, 2, 1}, 3))
}
