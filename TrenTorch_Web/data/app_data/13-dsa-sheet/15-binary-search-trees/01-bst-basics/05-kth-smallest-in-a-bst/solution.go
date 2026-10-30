package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(h + k) time, O(h) space where h is the tree height
func kthSmallestBst(root *TreeNode, k int) int {
	stack := []*TreeNode{}
	node := root
	for node != nil || len(stack) > 0 {
		for node != nil {
			stack = append(stack, node)
			node = node.Left
		}
		node = stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		k--
		if k == 0 {
			return node.Val
		}
		node = node.Right
	}
	return 0
}

func main() {
	// Call it here and print the result to try it.
}
