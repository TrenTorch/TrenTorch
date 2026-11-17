package main

import (
	"container/heap"
	"fmt"
)

type minIntHeap []int

func (h minIntHeap) Len() int           { return len(h) }
func (h minIntHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h minIntHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *minIntHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *minIntHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

// O(n log k) time, O(k) space
func medianSlidingWindow(nums []int, k int) []float64 {
	small := &minIntHeap{} // max-heap of the lower half (stored negated)
	large := &minIntHeap{} // min-heap of the upper half
	delayed := map[int]int{}
	size := [2]int{} // live sizes of small and large

	clean := func(h *minIntHeap, negated bool) {
		for h.Len() > 0 {
			value := (*h)[0]
			if negated {
				value = -value
			}
			if delayed[value] > 0 {
				delayed[value]--
				heap.Pop(h)
			} else {
				break
			}
		}
	}

	balance := func() {
		if size[0] > size[1]+1 {
			heap.Push(large, -(heap.Pop(small).(int)))
			size[0]--
			size[1]++
			clean(small, true)
		} else if size[0] < size[1] {
			heap.Push(small, -(heap.Pop(large).(int)))
			size[1]--
			size[0]++
			clean(large, false)
		}
	}

	add := func(x int) {
		if small.Len() == 0 || x <= -(*small)[0] {
			heap.Push(small, -x)
			size[0]++
		} else {
			heap.Push(large, x)
			size[1]++
		}
		balance()
	}

	remove := func(x int) {
		delayed[x]++
		if x <= -(*small)[0] {
			size[0]--
			if x == -(*small)[0] {
				clean(small, true)
			}
		} else {
			size[1]--
			if x == (*large)[0] {
				clean(large, false)
			}
		}
		balance()
	}

	median := func() float64 {
		if k%2 == 1 {
			return float64(-(*small)[0])
		}
		return float64(-(*small)[0]+(*large)[0]) / 2
	}

	for _, x := range nums[:k] {
		add(x)
	}
	out := []float64{median()}
	for i := k; i < len(nums); i++ {
		add(nums[i])
		remove(nums[i-k])
		out = append(out, median())
	}
	return out
}

func main() {
	fmt.Println(medianSlidingWindow([]int{1, 3, -1, -3, 5, 3, 6, 7}, 3))
}
