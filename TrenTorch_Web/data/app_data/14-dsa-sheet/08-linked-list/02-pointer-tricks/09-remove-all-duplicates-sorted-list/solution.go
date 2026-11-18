package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func removeAllDuplicates(head *ListNode) *ListNode {
	dummy := &ListNode{Val: 0, Next: head}
	prev, cur := dummy, head
	for cur != nil {
		if cur.Next != nil && cur.Next.Val == cur.Val {
			value := cur.Val
			for cur != nil && cur.Val == value {
				cur = cur.Next
			}
			prev.Next = cur
		} else {
			prev = cur
			cur = cur.Next
		}
	}
	return dummy.Next
}

func main() {
	// Call it here and print the result to try it.
}
