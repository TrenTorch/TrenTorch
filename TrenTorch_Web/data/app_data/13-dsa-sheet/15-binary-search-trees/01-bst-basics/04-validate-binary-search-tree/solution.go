package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(h) space for the recursion where h is the tree height
func isValidBst(root *TreeNode) bool {
	return validBstRange(root, -(1 << 62), 1<<62)
}

func validBstRange(node *TreeNode, low, high int) bool {
	if node == nil {
		return true
	}
	if !(low < node.Val && node.Val < high) {
		return false
	}
	return validBstRange(node.Left, low, node.Val) && validBstRange(node.Right, node.Val, high)
}

func main() {
	// Call it here and print the result to try it.
}
