package main

import "fmt"

// O(n) time, O(1) space
func largestOddNumber(num string) string {
	for i := len(num) - 1; i >= 0; i-- {
		d := num[i] - '0'
		if d%2 == 1 {
			return num[:i+1]
		}
	}
	return ""
}

func main() {
	fmt.Println(largestOddNumber("52"))
}
