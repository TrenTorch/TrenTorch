package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space where h is the tree height
func preorderTraversal(root *TreeNode) []int {
	out := []int{}
	stack := []*TreeNode{}
	if root != nil {
		stack = append(stack, root)
	}
	for len(stack) > 0 {
		node := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		out = append(out, node.Val)
		if node.Right != nil {
			stack = append(stack, node.Right)
		}
		if node.Left != nil {
			stack = append(stack, node.Left)
		}
	}
	return out
}

func main() {
	// Call it here and print the result to try it.
}
