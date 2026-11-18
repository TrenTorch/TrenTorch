package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

type depthItem struct {
	node  *TreeNode
	depth int
}

// O(n) time, O(n) space
func minDepth(root *TreeNode) int {
	if root == nil {
		return 0
	}
	queue := []depthItem{{root, 1}}
	for i := 0; i < len(queue); i++ {
		it := queue[i]
		if it.node.Left == nil && it.node.Right == nil {
			return it.depth
		}
		if it.node.Left != nil {
			queue = append(queue, depthItem{it.node.Left, it.depth + 1})
		}
		if it.node.Right != nil {
			queue = append(queue, depthItem{it.node.Right, it.depth + 1})
		}
	}
	return 0
}

func main() {
	// Call it here and print the result to try it.
}
