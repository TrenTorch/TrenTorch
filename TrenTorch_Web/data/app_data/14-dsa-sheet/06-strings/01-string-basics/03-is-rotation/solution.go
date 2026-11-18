package main

import (
	"fmt"
	"strings"
)

// O(n) time, O(n) space
func isRotation(s string, goal string) bool {
	return len(s) == len(goal) && strings.Contains(s+s, goal)
}

func main() {
	fmt.Println(isRotation("abcde", "cdeab"))
}
