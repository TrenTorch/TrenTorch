package main

import "fmt"

// O(n + m) time, O(n + m) space (two-pointer merge that skips repeated values).
func unionSorted(a []int, b []int) []int {
	out := make([]int, 0, len(a)+len(b))
	i, j := 0, 0
	for i < len(a) || j < len(b) {
		var x int
		if j == len(b) || (i < len(a) && a[i] <= b[j]) {
			x = a[i]
			i++
		} else {
			x = b[j]
			j++
		}
		if len(out) == 0 || out[len(out)-1] != x {
			out = append(out, x)
		}
	}
	return out
}

func main() {
	fmt.Println(unionSorted([]int{1, 2, 2, 4}, []int{2, 3, 4, 5}))
}
