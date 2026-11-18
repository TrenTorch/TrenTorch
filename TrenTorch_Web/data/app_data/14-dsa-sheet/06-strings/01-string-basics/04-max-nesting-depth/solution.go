package main

import "fmt"

// O(n) time, O(1) space
func maxNestingDepth(s string) int {
	depth, best := 0, 0
	for i := 0; i < len(s); i++ {
		if s[i] == '(' {
			depth++
			if depth > best {
				best = depth
			}
		} else if s[i] == ')' {
			depth--
		}
	}
	return best
}

func main() {
	fmt.Println(maxNestingDepth("(1+(2*3)+((8)/4))+1"))
}
