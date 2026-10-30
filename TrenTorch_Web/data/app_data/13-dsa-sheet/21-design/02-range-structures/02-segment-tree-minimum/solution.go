package main

import (
	"fmt"
	"math"
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
func runSegmentTree(nums []int, ops []string) []int {
	n := len(nums)
	const inf = math.MaxInt
	tree := make([]int, 2*n)
	for i := range tree {
		tree[i] = inf
	}
	copy(tree[n:], nums)
	for i := n - 1; i > 0; i-- {
		tree[i] = min(tree[2*i], tree[2*i+1])
	}
	out := []int{}
	for _, op := range ops {
		parts := strings.Fields(op)
		if parts[0] == "set" {
			i := mustAtoi(parts[1]) + n
			tree[i] = mustAtoi(parts[2])
			i /= 2
			for i >= 1 {
				tree[i] = min(tree[2*i], tree[2*i+1])
				i /= 2
			}
		} else {
			lo, hi := mustAtoi(parts[1])+n, mustAtoi(parts[2])+n+1
			best := inf
			for lo < hi {
				if lo&1 == 1 {
					best = min(best, tree[lo])
					lo++
				}
				if hi&1 == 1 {
					hi--
					best = min(best, tree[hi])
				}
				lo /= 2
				hi /= 2
			}
			out = append(out, best)
		}
	}
	return out
}

func main() {
	fmt.Println(runSegmentTree([]int{5, 2, 8, 1}, []string{"min 0 3", "set 3 9", "min 0 3", "min 2 3"}))
}
