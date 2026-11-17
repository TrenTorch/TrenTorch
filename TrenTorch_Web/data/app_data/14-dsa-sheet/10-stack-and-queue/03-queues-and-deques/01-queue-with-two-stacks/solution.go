package main

import (
	"fmt"
	"strconv"
	"strings"
)

// O(n) time overall (O(1) amortized per operation), O(n) space
func queueWithTwoStacks(ops []string) []int {
	inbox := []int{}
	outbox := []int{}
	out := []int{}
	move := func() {
		if len(outbox) == 0 {
			for len(inbox) > 0 {
				outbox = append(outbox, inbox[len(inbox)-1])
				inbox = inbox[:len(inbox)-1]
			}
		}
	}
	for _, op := range ops {
		if strings.HasPrefix(op, "push") {
			x, err := strconv.Atoi(strings.Fields(op)[1])
			if err != nil {
				panic(err)
			}
			inbox = append(inbox, x)
		} else if op == "pop" {
			move()
			out = append(out, outbox[len(outbox)-1])
			outbox = outbox[:len(outbox)-1]
		} else if op == "peek" {
			move()
			out = append(out, outbox[len(outbox)-1])
		} else {
			if len(inbox) == 0 && len(outbox) == 0 {
				out = append(out, 1)
			} else {
				out = append(out, 0)
			}
		}
	}
	return out
}

func main() {
	fmt.Println(queueWithTwoStacks([]string{"push 1", "push 2", "peek", "pop", "empty"}))
}
