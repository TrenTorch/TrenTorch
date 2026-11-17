package main

import "fmt"

// O(n) time, O(n) space
func countPalindromesFast(s string) int {
	n := len(s)
	total := 0
	d1 := make([]int, n)
	left, right := 0, -1
	for i := 0; i < n; i++ {
		k := 1
		if i <= right {
			k = min(d1[left+right-i], right-i+1)
		}
		for i-k >= 0 && i+k < n && s[i-k] == s[i+k] {
			k++
		}
		d1[i] = k
		total += k
		if i+k-1 > right {
			left, right = i-k+1, i+k-1
		}
	}
	d2 := make([]int, n)
	left, right = 0, -1
	for i := 0; i < n; i++ {
		k := 0
		if i <= right {
			k = min(d2[left+right-i+1], right-i+1)
		}
		for i-k-1 >= 0 && i+k < n && s[i-k-1] == s[i+k] {
			k++
		}
		d2[i] = k
		total += k
		if i+k-1 > right {
			left, right = i-k, i+k-1
		}
	}
	return total
}

func main() {
	fmt.Println(countPalindromesFast("aaa"))
}
