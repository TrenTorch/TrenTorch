package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(n) space
func rightSideView(root *TreeNode) []int {
	out := []int{}
	if root == nil {
		return out
	}
	queue := []*TreeNode{root}
	for len(queue) > 0 {
		n := len(queue)
		last := 0
		for i := 0; i < n; i++ {
			node := queue[i]
			last = node.Val
			if node.Left != nil {
				queue = append(queue, node.Left)
			}
			if node.Right != nil {
				queue = append(queue, node.Right)
			}
		}
		queue = queue[n:]
		out = append(out, last)
	}
	return out
}

func main() {
	// Call it here and print the result to try it.
}
