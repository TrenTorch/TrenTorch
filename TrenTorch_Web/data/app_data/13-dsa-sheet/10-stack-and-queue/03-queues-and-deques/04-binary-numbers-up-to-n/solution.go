package main

import "fmt"

// O(n) time, O(n) space
func binaryNumbersUpTo(n int) []string {
	out := []string{}
	queue := []string{"1"}
	head := 0
	for i := 0; i < n; i++ {
		front := queue[head]
		head++
		out = append(out, front)
		queue = append(queue, front+"0", front+"1")
	}
	return out
}

func main() {
	fmt.Println(binaryNumbersUpTo(5))
}
