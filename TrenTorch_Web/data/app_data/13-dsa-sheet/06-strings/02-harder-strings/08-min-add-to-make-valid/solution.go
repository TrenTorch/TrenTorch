package main

import "fmt"

// O(n) time, O(1) space
func minAddToMakeValid(s string) int {
	openCount, need := 0, 0
	for i := 0; i < len(s); i++ {
		if s[i] == '(' {
			openCount++
		} else if openCount > 0 {
			openCount--
		} else {
			need++
		}
	}
	return need + openCount
}

func main() {
	fmt.Println(minAddToMakeValid("())"))
}
