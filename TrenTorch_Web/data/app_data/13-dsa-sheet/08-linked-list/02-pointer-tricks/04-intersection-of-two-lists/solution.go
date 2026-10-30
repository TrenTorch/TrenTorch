package main

type ListNode struct {
	Val  int
	Next *ListNode
}

// O(m + n) time, O(1) space
func intersectionNode(listA, listB *ListNode) *ListNode {
	pa, pb := listA, listB
	for pa != pb {
		if pa != nil {
			pa = pa.Next
		} else {
			pa = listB
		}
		if pb != nil {
			pb = pb.Next
		} else {
			pb = listA
		}
	}
	return pa
}

func main() {
}
