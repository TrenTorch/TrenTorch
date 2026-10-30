package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

// O(n) time, O(n) space
func burnTime(root *TreeNode, start int) int {
	parent := map[*TreeNode]*TreeNode{root: nil}
	var origin *TreeNode
	stack := []*TreeNode{root}
	for len(stack) > 0 {
		node := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if node.Val == start {
			origin = node
		}
		if node.Left != nil {
			parent[node.Left] = node
			stack = append(stack, node.Left)
		}
		if node.Right != nil {
			parent[node.Right] = node
			stack = append(stack, node.Right)
		}
	}
	seen := map[*TreeNode]bool{origin: true}
	frontier := []*TreeNode{origin}
	minutes := -1
	for len(frontier) > 0 {
		minutes++
		next := []*TreeNode{}
		for _, node := range frontier {
			for _, nxt := range []*TreeNode{node.Left, node.Right, parent[node]} {
				if nxt != nil && !seen[nxt] {
					seen[nxt] = true
					next = append(next, nxt)
				}
			}
		}
		frontier = next
	}
	return minutes
}

func main() {
	// Call it here and print the result to try it.
}
