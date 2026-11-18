package main

import "fmt"

// sortCount returns the sorted copy of a and the number of inversions in a (merge sort).
func sortCount(a []int) ([]int, int) {
	if len(a) <= 1 {
		return a, 0
	}
	mid := len(a) / 2
	left, x := sortCount(a[:mid])
	right, y := sortCount(a[mid:])
	merged := make([]int, 0, len(a))
	i, j, cross := 0, 0, 0
	for i < len(left) && j < len(right) {
		if left[i] <= right[j] {
			merged = append(merged, left[i])
			i++
		} else {
			merged = append(merged, right[j])
			j++
			cross += len(left) - i
		}
	}
	merged = append(merged, left[i:]...)
	merged = append(merged, right[j:]...)
	return merged, x + y + cross
}

// O(n log n) time, O(n) space (merge sort that counts cross-half inversions).
func countInversions(nums []int) int {
	_, total := sortCount(append([]int(nil), nums...))
	return total
}

func main() {
	fmt.Println(countInversions([]int{3, 1, 2}))
}
