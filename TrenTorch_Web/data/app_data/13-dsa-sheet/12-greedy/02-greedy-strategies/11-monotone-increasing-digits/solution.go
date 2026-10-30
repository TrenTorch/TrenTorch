package main

import (
	"fmt"
	"strconv"
)

// O(d) time, O(d) space where d is the number of digits of n
func monotoneIncreasingDigits(n int) int {
	digits := []byte(strconv.Itoa(n))
	mark := len(digits)
	for i := len(digits) - 1; i > 0; i-- {
		if digits[i-1] > digits[i] {
			digits[i-1]--
			mark = i
		}
	}
	for i := mark; i < len(digits); i++ {
		digits[i] = '9'
	}
	result, err := strconv.Atoi(string(digits))
	if err != nil {
		panic(err)
	}
	return result
}

func main() {
	fmt.Println(monotoneIncreasingDigits(332))
}
