package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func removeDuplicatesSorted(head *ListNode) *ListNode {
	cur := head
	for cur != nil && cur.Next != nil {
		if cur.Val == cur.Next.Val {
			cur.Next = cur.Next.Next
		} else {
			cur = cur.Next
		}
	}
	return head
}

func main() {
	// Call it here and print the result to try it.
}
