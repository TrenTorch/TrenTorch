package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(n) space
func zigzagLevelOrder(root *TreeNode) [][]int {
	out := [][]int{}
	if root == nil {
		return out
	}
	queue := []*TreeNode{root}
	leftToRight := true
	for len(queue) > 0 {
		n := len(queue)
		level := []int{}
		for i := 0; i < n; i++ {
			node := queue[i]
			level = append(level, node.Val)
			if node.Left != nil {
				queue = append(queue, node.Left)
			}
			if node.Right != nil {
				queue = append(queue, node.Right)
			}
		}
		queue = queue[n:]
		if !leftToRight {
			for i, j := 0, len(level)-1; i < j; i, j = i+1, j-1 {
				level[i], level[j] = level[j], level[i]
			}
		}
		out = append(out, level)
		leftToRight = !leftToRight
	}
	return out
}

func main() {
	// Call it here and print the result to try it.
}
