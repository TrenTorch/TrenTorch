package main

import "fmt"

// O(1) time, O(1) space (the output is at most 15 characters)
func integerToRoman(num int) string {
	values := []int{1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1}
	symbols := []string{"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"}
	var out []byte
	for i, value := range values {
		count := num / value
		num %= value
		for c := 0; c < count; c++ {
			out = append(out, symbols[i]...)
		}
	}
	return string(out)
}

func main() {
	fmt.Println(integerToRoman(3))
}
