package main

import "fmt"

// O(row^2) time for the row values' arithmetic, O(row) space; note: int overflows for row > 66 (Python big ints do not)
func pascalRow(row int) []int {
	out := []int{}
	value := 1
	for i := 0; i <= row; i++ {
		out = append(out, value)
		value = value * (row - i) / (i + 1)
	}
	return out
}

func main() {
	fmt.Println(pascalRow(4))
}
