package main

import "sort"

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n log n) time, O(n) space
func distanceK(root *TreeNode, target int, k int) []int {
	parent := map[*TreeNode]*TreeNode{root: nil}
	var start *TreeNode
	stack := []*TreeNode{root}
	for len(stack) > 0 {
		node := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if node.Val == target {
			start = node
		}
		if node.Left != nil {
			parent[node.Left] = node
			stack = append(stack, node.Left)
		}
		if node.Right != nil {
			parent[node.Right] = node
			stack = append(stack, node.Right)
		}
	}
	seen := map[*TreeNode]bool{start: true}
	frontier := []*TreeNode{start}
	for step := 0; step < k; step++ {
		next := []*TreeNode{}
		for _, node := range frontier {
			for _, nxt := range []*TreeNode{node.Left, node.Right, parent[node]} {
				if nxt != nil && !seen[nxt] {
					seen[nxt] = true
					next = append(next, nxt)
				}
			}
		}
		frontier = next
	}
	out := make([]int, 0, len(frontier))
	for _, node := range frontier {
		out = append(out, node.Val)
	}
	sort.Ints(out)
	return out
}

func main() {
	// Call it here and print the result to try it.
}
