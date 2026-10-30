package main

import "fmt"

// O(sqrt(n)) time, O(1) space
func eulerPhi(n int) int {
	result := n
	d := 2
	for d*d <= n {
		if n%d == 0 {
			for n%d == 0 {
				n /= d
			}
			result -= result / d
		}
		if d == 2 {
			d++
		} else {
			d += 2
		}
	}
	if n > 1 {
		result -= result / n
	}
	return result
}

func main() {
	fmt.Println(eulerPhi(12))
}
