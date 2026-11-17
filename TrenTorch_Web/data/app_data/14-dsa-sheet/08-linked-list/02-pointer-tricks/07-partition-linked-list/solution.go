package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(n) time, O(1) space
func partitionList(head *ListNode, x int) *ListNode {
	smallDummy := &ListNode{}
	largeDummy := &ListNode{}
	smallTail, largeTail := smallDummy, largeDummy
	for head != nil {
		if head.Val < x {
			smallTail.Next = head
			smallTail = head
		} else {
			largeTail.Next = head
			largeTail = head
		}
		head = head.Next
	}
	largeTail.Next = nil
	smallTail.Next = largeDummy.Next
	return smallDummy.Next
}

func main() {
	// Call it here and print the result to try it.
}
