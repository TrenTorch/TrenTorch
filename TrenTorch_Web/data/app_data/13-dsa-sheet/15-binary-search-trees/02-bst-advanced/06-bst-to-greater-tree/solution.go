package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space where h is the tree height
func convertBst(root *TreeNode) *TreeNode {
	total := 0
	stack := []*TreeNode{}
	node := root
	for node != nil || len(stack) > 0 {
		for node != nil {
			stack = append(stack, node)
			node = node.Right
		}
		node = stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		total += node.Val
		node.Val = total
		node = node.Left
	}
	return root
}

func main() {
	// Call it here and print the result to try it.
}
