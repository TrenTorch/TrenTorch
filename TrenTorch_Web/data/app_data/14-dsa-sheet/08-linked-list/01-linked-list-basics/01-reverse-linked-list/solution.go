package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func reverseList(head *ListNode) *ListNode {
	var prev *ListNode
	for head != nil {
		after := head.Next
		head.Next = prev
		prev = head
		head = after
	}
	return prev
}

func main() {
	// Call it here and print the result to try it.
}
