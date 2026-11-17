package main

import "fmt"

type xorNode struct {
	child [2]*xorNode
}

// O(30 * (N + Q)) time, O(30 * N) space
func maxXorQueries(nums []int, queries []int) []int {
	root := &xorNode{}
	for _, n := range nums {
		node := root
		for b := 29; b >= 0; b-- {
			bit := (n >> b) & 1
			if node.child[bit] == nil {
				node.child[bit] = &xorNode{}
			}
			node = node.child[bit]
		}
	}
	out := make([]int, 0, len(queries))
	for _, x := range queries {
		node := root
		best := 0
		for b := 29; b >= 0; b-- {
			bit := (x >> b) & 1
			if node.child[1-bit] != nil {
				best |= 1 << b
				node = node.child[1-bit]
			} else {
				node = node.child[bit]
			}
		}
		out = append(out, best)
	}
	return out
}

func main() {
	fmt.Println(maxXorQueries([]int{0, 1, 2, 3, 4}, []int{3, 5}))
}
