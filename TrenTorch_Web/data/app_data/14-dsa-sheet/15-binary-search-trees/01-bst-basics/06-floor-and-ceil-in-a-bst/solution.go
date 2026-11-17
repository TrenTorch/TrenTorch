package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(h) time, O(1) space where h is the tree height
func floorAndCeilBst(root *TreeNode, x int) []int {
	floor, ceil := -1, -1
	node := root
	for node != nil {
		if node.Val == x {
			return []int{x, x}
		}
		if node.Val < x {
			floor = node.Val
			node = node.Right
		} else {
			ceil = node.Val
			node = node.Left
		}
	}
	return []int{floor, ceil}
}

func main() {
	// Call it here and print the result to try it.
}
