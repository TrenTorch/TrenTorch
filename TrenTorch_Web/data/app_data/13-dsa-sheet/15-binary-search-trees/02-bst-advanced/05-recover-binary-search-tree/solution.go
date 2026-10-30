package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space where h is the tree height
func recoverTree(root *TreeNode) *TreeNode {
	var first, second, prev *TreeNode
	stack := []*TreeNode{}
	node := root
	for node != nil || len(stack) > 0 {
		for node != nil {
			stack = append(stack, node)
			node = node.Left
		}
		node = stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if prev != nil && prev.Val > node.Val {
			if first == nil {
				first = prev
			}
			second = node
		}
		prev = node
		node = node.Right
	}
	first.Val, second.Val = second.Val, first.Val
	return root
}

func main() {
	// Call it here and print the result to try it.
}
