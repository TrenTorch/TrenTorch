package main

import (
	"fmt"
	"strconv"
)

// O(log n) time, O(1) space (plus the digits of one number)
func nthDigit(n int) int {
	length, count, start := 1, 9, 1
	for n > length*count {
		n -= length * count
		length++
		count *= 10
		start *= 10
	}
	number := start + (n-1)/length
	s := strconv.Itoa(number)
	return int(s[(n-1)%length] - '0')
}

func main() {
	fmt.Println(nthDigit(11))
}
