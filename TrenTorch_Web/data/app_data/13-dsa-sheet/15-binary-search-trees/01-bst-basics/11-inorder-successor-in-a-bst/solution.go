package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(h) time, O(1) space where h is the tree height
func inorderSuccessor(root *TreeNode, p int) *TreeNode {
	var answer *TreeNode
	node := root
	for node != nil {
		if node.Val > p {
			answer = node
			node = node.Left
		} else {
			node = node.Right
		}
	}
	return answer
}

func main() {
}
