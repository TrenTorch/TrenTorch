package main

import "fmt"

// O(n!) time worst case, O(n) extra space
func nQueensCount(n int) int {
	cols := make([]bool, n)
	diag1 := make([]bool, 2*n)
	diag2 := make([]bool, 2*n)
	var rec func(r int) int
	rec = func(r int) int {
		if r == n {
			return 1
		}
		total := 0
		for c := 0; c < n; c++ {
			d1 := r - c + n - 1
			d2 := r + c
			if cols[c] || diag1[d1] || diag2[d2] {
				continue
			}
			cols[c], diag1[d1], diag2[d2] = true, true, true
			total += rec(r + 1)
			cols[c], diag1[d1], diag2[d2] = false, false, false
		}
		return total
	}
	return rec(0)
}

func main() {
	fmt.Println(nQueensCount(4))
}
