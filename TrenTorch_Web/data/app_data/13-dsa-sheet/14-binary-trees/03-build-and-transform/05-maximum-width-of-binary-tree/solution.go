package main

type TreeNode struct {
	Val         int
	Left, Right *TreeNode
}

type widthItem struct {
	node *TreeNode
	idx  int
}

// O(n) time, O(w) space where w is the widest level
func widthOfTree(root *TreeNode) int {
	if root == nil {
		return 0
	}
	best := 0
	level := []widthItem{{root, 0}}
	for len(level) > 0 {
		first := level[0].idx
		last := 0
		next := make([]widthItem, 0, 2*len(level))
		for _, it := range level {
			rel := it.idx - first
			last = rel
			if it.node.Left != nil {
				next = append(next, widthItem{it.node.Left, 2 * rel})
			}
			if it.node.Right != nil {
				next = append(next, widthItem{it.node.Right, 2*rel + 1})
			}
		}
		if last+1 > best {
			best = last + 1
		}
		level = next
	}
	return best
}

func main() {
	// Call it here and print the result to try it.
}
