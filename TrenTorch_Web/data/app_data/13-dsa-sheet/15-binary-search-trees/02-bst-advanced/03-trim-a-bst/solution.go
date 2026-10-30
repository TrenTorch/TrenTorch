package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space for the recursion where h is the tree height
func trimBst(root *TreeNode, low int, high int) *TreeNode {
	if root == nil {
		return nil
	}
	if root.Val < low {
		return trimBst(root.Right, low, high)
	}
	if root.Val > high {
		return trimBst(root.Left, low, high)
	}
	root.Left = trimBst(root.Left, low, high)
	root.Right = trimBst(root.Right, low, high)
	return root
}

func main() {
	// Call it here and print the result to try it.
}
