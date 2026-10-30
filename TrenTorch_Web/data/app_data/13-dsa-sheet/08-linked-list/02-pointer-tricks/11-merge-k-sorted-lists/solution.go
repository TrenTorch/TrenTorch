package main

import "container/heap"

type ListNode struct {
	Val  int
	Next *ListNode
}

type nodeHeap []*ListNode

func (h nodeHeap) Len() int           { return len(h) }
func (h nodeHeap) Less(i, j int) bool { return h[i].Val < h[j].Val }
func (h nodeHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *nodeHeap) Push(x any) {
	*h = append(*h, x.(*ListNode))
}

func (h *nodeHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

// O(N log k) time for N total nodes and k lists, O(k) space
func mergeKLists(lists []*ListNode) *ListNode {
	h := &nodeHeap{}
	for _, node := range lists {
		if node != nil {
			*h = append(*h, node)
		}
	}
	heap.Init(h)
	dummy := &ListNode{}
	tail := dummy
	for h.Len() > 0 {
		node := heap.Pop(h).(*ListNode)
		tail.Next = node
		tail = node
		if node.Next != nil {
			heap.Push(h, node.Next)
		}
	}
	return dummy.Next
}

func main() {
}
