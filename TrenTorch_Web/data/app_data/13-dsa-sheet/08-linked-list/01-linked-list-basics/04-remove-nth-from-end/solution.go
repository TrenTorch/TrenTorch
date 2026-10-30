package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func removeNthFromEnd(head *ListNode, n int) *ListNode {
	dummy := &ListNode{Val: 0, Next: head}
	fast, slow := dummy, dummy
	for i := 0; i < n; i++ {
		fast = fast.Next
	}
	for fast.Next != nil {
		fast = fast.Next
		slow = slow.Next
	}
	slow.Next = slow.Next.Next
	return dummy.Next
}

func main() {
	// Call it here and print the result to try it.
}
