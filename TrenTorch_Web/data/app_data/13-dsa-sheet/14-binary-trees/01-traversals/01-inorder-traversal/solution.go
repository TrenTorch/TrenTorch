package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space where h is the tree height
func inorderTraversal(root *TreeNode) []int {
	out := []int{}
	stack := []*TreeNode{}
	node := root
	for node != nil || len(stack) > 0 {
		for node != nil {
			stack = append(stack, node)
			node = node.Left
		}
		node = stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		out = append(out, node.Val)
		node = node.Right
	}
	return out
}

func main() {
	// Call it here and print the result to try it.
}
