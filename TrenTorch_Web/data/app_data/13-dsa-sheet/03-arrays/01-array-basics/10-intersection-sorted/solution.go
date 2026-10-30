package main

import "fmt"

// O(n + m) time, O(min(n, m)) space for the output
func intersectionSorted(a []int, b []int) []int {
	out := []int{}
	i, j := 0, 0
	for i < len(a) && j < len(b) {
		if a[i] == b[j] {
			out = append(out, a[i])
			i++
			j++
		} else if a[i] < b[j] {
			i++
		} else {
			j++
		}
	}
	return out
}

func main() {
	fmt.Println(intersectionSorted([]int{1, 2, 2, 3}, []int{2, 2, 2, 4}))
}
