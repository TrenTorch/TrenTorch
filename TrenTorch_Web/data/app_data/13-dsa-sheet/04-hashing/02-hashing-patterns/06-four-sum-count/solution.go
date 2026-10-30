package main

import "fmt"

// O(n^2) time, O(n^2) space
func fourSumCount(a []int, b []int, c []int, d []int) int {
	sums := make(map[int]int, len(a)*len(b))
	for _, x := range a {
		for _, y := range b {
			sums[x+y]++
		}
	}
	count := 0
	for _, z := range c {
		for _, w := range d {
			count += sums[-(z + w)]
		}
	}
	return count
}

func main() {
	fmt.Println(fourSumCount([]int{1, 2}, []int{-2, -1}, []int{-1, 2}, []int{0, 2}))
}
