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

// O(q log n) time, O(n) space
func runRangeAdd(n int, ops []string) []int {
	tree := make([]int, n+2)

	add := func(i, delta int) {
		i++
		for i <= n+1 {
			tree[i] += delta
			i += i & -i
		}
	}

	prefix := func(i int) int {
		total := 0
		i++
		for i > 0 {
			total += tree[i]
			i -= i & -i
		}
		return total
	}

	out := []int{}
	for _, op := range ops {
		parts := strings.Fields(op)
		if parts[0] == "add" {
			left, right, v := mustAtoi(parts[1]), mustAtoi(parts[2]), mustAtoi(parts[3])
			add(left, v)
			add(right+1, -v)
		} else {
			out = append(out, prefix(mustAtoi(parts[1])))
		}
	}
	return out
}

func main() {
	fmt.Println(runRangeAdd(5, []string{"add 1 3 10", "get 2", "add 0 4 -1", "get 0", "get 3"}))
}
