package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(max(n, m)) time, O(max(n, m)) space for the result
func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
	dummy := &ListNode{}
	tail := dummy
	carry := 0
	for l1 != nil || l2 != nil || carry != 0 {
		total := carry
		if l1 != nil {
			total += l1.Val
			l1 = l1.Next
		}
		if l2 != nil {
			total += l2.Val
			l2 = l2.Next
		}
		tail.Next = &ListNode{Val: total % 10}
		tail = tail.Next
		carry = total / 10
	}
	return dummy.Next
}

func main() {
	// Call it here and print the result to try it.
}
