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

// O(n + q log n) time, O(n) space
func runFenwick(nums []int, ops []string) []int {
	n := len(nums)
	tree := make([]int, n+1)
	values := append([]int(nil), nums...)

	add := func(i, delta int) {
		i++
		for i <= n {
			tree[i] += delta
			i += i & -i
		}
	}

	prefix := func(i int) int {
		total := 0
		for i > 0 {
			total += tree[i]
			i -= i & -i
		}
		return total
	}

	for i, x := range nums {
		add(i, x)
	}
	out := []int{}
	for _, op := range ops {
		parts := strings.Fields(op)
		if parts[0] == "set" {
			i, v := mustAtoi(parts[1]), mustAtoi(parts[2])
			add(i, v-values[i])
			values[i] = v
		} else {
			left, right := mustAtoi(parts[1]), mustAtoi(parts[2])
			out = append(out, prefix(right+1)-prefix(left))
		}
	}
	return out
}

func main() {
	fmt.Println(runFenwick([]int{1, 2, 3, 4}, []string{"sum 0 3", "set 1 10", "sum 0 2", "sum 1 1"}))
}
