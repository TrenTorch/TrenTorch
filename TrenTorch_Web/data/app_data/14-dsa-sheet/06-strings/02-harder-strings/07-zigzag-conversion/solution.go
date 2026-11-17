package main

import "fmt"

// O(n) time, O(n) space
func zigzagConversion(s string, rows int) string {
	if rows == 1 || rows >= len(s) {
		return s
	}
	lines := make([][]byte, rows)
	row, step := 0, 1
	for i := 0; i < len(s); i++ {
		lines[row] = append(lines[row], s[i])
		if row == 0 {
			step = 1
		} else if row == rows-1 {
			step = -1
		}
		row += step
	}
	var out []byte
	for _, line := range lines {
		out = append(out, line...)
	}
	return string(out)
}

func main() {
	fmt.Println(zigzagConversion("PAYPALISHIRING", 3))
}
