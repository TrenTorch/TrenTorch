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

// O(q α(n)) time, O(n) space
func runUnionFind(n int, ops []string) []int {
	parent := make([]int, n)
	size := make([]int, n)
	for i := range parent {
		parent[i] = i
		size[i] = 1
	}

	find := func(x int) int {
		for parent[x] != x {
			parent[x] = parent[parent[x]]
			x = parent[x]
		}
		return x
	}

	out := []int{}
	for _, op := range ops {
		parts := strings.Fields(op)
		switch parts[0] {
		case "union":
			a, b := find(mustAtoi(parts[1])), find(mustAtoi(parts[2]))
			if a != b {
				if size[a] < size[b] {
					a, b = b, a
				}
				parent[b] = a
				size[a] += size[b]
			}
		case "connected":
			if find(mustAtoi(parts[1])) == find(mustAtoi(parts[2])) {
				out = append(out, 1)
			} else {
				out = append(out, 0)
			}
		default:
			out = append(out, size[find(mustAtoi(parts[1]))])
		}
	}
	return out
}

func main() {
	fmt.Println(runUnionFind(5, []string{"union 0 1", "union 1 2", "connected 0 2", "connected 0 3", "size 2"}))
}
