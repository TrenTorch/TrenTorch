package main

import (
	"fmt"
	"strconv"
	"strings"
)

func mustAtoi(s string) int {
	v, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return v
}

// O(1) time per operation, O(n) space for the history
func runBrowserHistory(homepage string, ops []string) []string {
	history := []string{homepage}
	index := 0
	out := []string{}
	for _, op := range ops {
		parts := strings.Fields(op)
		kind, arg := parts[0], parts[1]
		switch kind {
		case "visit":
			history = append(history[:index+1], arg)
			index++
		case "back":
			index = max(0, index-mustAtoi(arg))
			out = append(out, history[index])
		default:
			index = min(len(history)-1, index+mustAtoi(arg))
			out = append(out, history[index])
		}
	}
	return out
}

func main() {
	fmt.Println(runBrowserHistory("a", []string{"visit b", "visit c", "back 1", "back 5", "forward 1", "visit d", "forward 3"}))
}
