package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func middleNode(head *ListNode) *ListNode {
	slow, fast := head, head
	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
	}
	return slow
}

func main() {
	// Call it here and print the result to try it.
}
