package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space for the recursion where h is the tree height
func rangeSumBst(root *TreeNode, low int, high int) int {
	if root == nil {
		return 0
	}
	if root.Val < low {
		return rangeSumBst(root.Right, low, high)
	}
	if root.Val > high {
		return rangeSumBst(root.Left, low, high)
	}
	return root.Val + rangeSumBst(root.Left, low, high) + rangeSumBst(root.Right, low, high)
}

func main() {
	// Call it here and print the result to try it.
}
