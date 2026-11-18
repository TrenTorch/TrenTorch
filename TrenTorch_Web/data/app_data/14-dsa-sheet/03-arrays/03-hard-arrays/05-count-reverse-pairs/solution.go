package main

import "fmt"

// O(n log n) time, O(n) space
func countReversePairs(nums []int) int {
	a := make([]int, len(nums))
	copy(a, nums)
	buf := make([]int, len(a))
	return mergeCountReversePairs(a, buf)
}

// sorts a ascending in place and returns the number of reverse pairs inside a
func mergeCountReversePairs(a, buf []int) int {
	n := len(a)
	if n <= 1 {
		return 0
	}
	mid := n / 2
	count := mergeCountReversePairs(a[:mid], buf[:mid]) + mergeCountReversePairs(a[mid:], buf[mid:])
	j := 0
	for i := 0; i < mid; i++ {
		for j < n-mid && a[i] > 2*a[mid+j] {
			j++
		}
		count += j
	}
	i, k, m := 0, 0, mid
	for i < mid && m < n {
		if a[i] <= a[m] {
			buf[k] = a[i]
			i++
		} else {
			buf[k] = a[m]
			m++
		}
		k++
	}
	for i < mid {
		buf[k] = a[i]
		i++
		k++
	}
	for m < n {
		buf[k] = a[m]
		m++
		k++
	}
	copy(a, buf[:n])
	return count
}

func main() {
	fmt.Println(countReversePairs([]int{1, 3, 2, 3, 1}))
}
