package main

import "fmt"

// O(C(n,k) * k) time, O(C(n,k) * k) space for the output, O(k) extra space
func allCombinations(n int, k int) [][]int {
	out := [][]int{}
	current := []int{}
	var gen func(start int)
	gen = func(start int) {
		need := k - len(current)
		if need == 0 {
			out = append(out, append([]int(nil), current...))
			return
		}
		for j := start; j <= n-need+1; j++ {
			current = append(current, j)
			gen(j + 1)
			current = current[:len(current)-1]
		}
	}
	gen(1)
	return out
}

func main() {
	fmt.Println(allCombinations(4, 2))
}
