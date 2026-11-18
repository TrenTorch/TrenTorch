package main

import "fmt"

// O(sqrt(n)) time, O(log n) space
func primeFactors(n int) [][]int {
	out := [][]int{}
	d := 2
	for d*d <= n {
		if n%d == 0 {
			e := 0
			for n%d == 0 {
				n /= d
				e++
			}
			out = append(out, []int{d, e})
		}
		if d == 2 {
			d++
		} else {
			d += 2
		}
	}
	if n > 1 {
		out = append(out, []int{n, 1})
	}
	return out
}

func main() {
	fmt.Println(primeFactors(360))
}
