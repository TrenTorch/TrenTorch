package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space where h is the tree height
func minDiffBst(root *TreeNode) int {
	best := 1 << 62
	prev := 0
	hasPrev := false
	stack := []*TreeNode{}
	node := root
	for node != nil || len(stack) > 0 {
		for node != nil {
			stack = append(stack, node)
			node = node.Left
		}
		node = stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if hasPrev && node.Val-prev < best {
			best = node.Val - prev
		}
		prev = node.Val
		hasPrev = true
		node = node.Right
	}
	return best
}

func main() {
	// Call it here and print the result to try it.
}
