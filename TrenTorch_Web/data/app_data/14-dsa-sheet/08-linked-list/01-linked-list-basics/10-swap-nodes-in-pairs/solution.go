package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func swapPairs(head *ListNode) *ListNode {
	dummy := &ListNode{Val: 0, Next: head}
	prev := dummy
	for prev.Next != nil && prev.Next.Next != nil {
		a := prev.Next
		b := a.Next
		a.Next = b.Next
		b.Next = a
		prev.Next = b
		prev = a
	}
	return dummy.Next
}

func main() {
	// Call it here and print the result to try it.
}
