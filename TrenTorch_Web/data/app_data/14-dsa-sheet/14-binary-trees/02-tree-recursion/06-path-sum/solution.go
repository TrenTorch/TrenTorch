package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space
func hasPathSum(root *TreeNode, target int) bool {
	if root == nil {
		return false
	}
	if root.Left == nil && root.Right == nil {
		return root.Val == target
	}
	rest := target - root.Val
	return hasPathSum(root.Left, rest) || hasPathSum(root.Right, rest)
}

func main() {
	// Call it here and print the result to try it.
}
