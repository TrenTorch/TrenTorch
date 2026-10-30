package main

import (
	"fmt"
	"strconv"
	"strings"
)

// O(n) time, O(n) space
func minStack(ops []string) []int {
	values := []int{}
	mins := []int{}
	out := []int{}
	for _, op := range ops {
		if strings.HasPrefix(op, "push") {
			x, err := strconv.Atoi(strings.Fields(op)[1])
			if err != nil {
				panic(err)
			}
			values = append(values, x)
			if len(mins) > 0 {
				mins = append(mins, min(x, mins[len(mins)-1]))
			} else {
				mins = append(mins, x)
			}
		} else if op == "pop" {
			values = values[:len(values)-1]
			mins = mins[:len(mins)-1]
		} else if op == "top" {
			out = append(out, values[len(values)-1])
		} else {
			out = append(out, mins[len(mins)-1])
		}
	}
	return out
}

func main() {
	fmt.Println(minStack([]string{"push 5", "push 3", "get_min", "pop", "top", "get_min"}))
}
