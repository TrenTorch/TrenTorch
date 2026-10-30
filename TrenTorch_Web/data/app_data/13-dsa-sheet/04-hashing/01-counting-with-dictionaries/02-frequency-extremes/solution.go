package main

import "fmt"

// O(n) time, O(n) space
func frequencyExtremes(nums []int) []int {
	counts := map[int]int{}
	for _, x := range nums {
		counts[x]++
	}
	first := true
	most, least := 0, 0
	mostCount, leastCount := 0, 0
	for v, c := range counts {
		if first {
			most, least, mostCount, leastCount = v, v, c, c
			first = false
			continue
		}
		if c > mostCount || (c == mostCount && v < most) {
			most, mostCount = v, c
		}
		if c < leastCount || (c == leastCount && v < least) {
			least, leastCount = v, c
		}
	}
	return []int{most, least}
}

func main() {
	fmt.Println(frequencyExtremes([]int{4, 4, 5, 5, 6}))
}
