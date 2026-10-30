package main

import "fmt"

// O(n) time, O(n) space
func nthUglyNumber(n int) int {
	ugly := []int{1}
	i2, i3, i5 := 0, 0, 0
	for len(ugly) < n {
		next := min(ugly[i2]*2, ugly[i3]*3, ugly[i5]*5)
		ugly = append(ugly, next)
		if next == ugly[i2]*2 {
			i2++
		}
		if next == ugly[i3]*3 {
			i3++
		}
		if next == ugly[i5]*5 {
			i5++
		}
	}
	return ugly[n-1]
}

func main() {
	fmt.Println(nthUglyNumber(10))
}
