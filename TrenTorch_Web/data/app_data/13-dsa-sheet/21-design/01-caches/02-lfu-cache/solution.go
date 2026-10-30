package main

import (
	"container/list"
	"fmt"
	"strconv"
	"strings"
)

type lfuEntry struct {
	key, value, count int
}

func mustAtoi(s string) int {
	v, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return v
}

// O(1) time per operation, O(capacity) space
func runLfu(capacity int, ops []string) []int {
	nodes := make(map[int]*list.Element)
	buckets := make(map[int]*list.List)
	low := 0

	touch := func(key int) {
		el := nodes[key]
		e := el.Value.(*lfuEntry)
		c := e.count
		b := buckets[c]
		b.Remove(el)
		if b.Len() == 0 {
			delete(buckets, c)
			if low == c {
				low++
			}
		}
		e.count = c + 1
		nb, ok := buckets[c+1]
		if !ok {
			nb = list.New()
			buckets[c+1] = nb
		}
		nodes[key] = nb.PushBack(e)
	}

	out := []int{}
	for _, op := range ops {
		parts := strings.Fields(op)
		key := mustAtoi(parts[1])
		if parts[0] == "get" {
			if _, ok := nodes[key]; ok {
				touch(key)
				out = append(out, nodes[key].Value.(*lfuEntry).value)
			} else {
				out = append(out, -1)
			}
		} else if capacity > 0 {
			value := mustAtoi(parts[2])
			if el, ok := nodes[key]; ok {
				el.Value.(*lfuEntry).value = value
				touch(key)
			} else {
				if len(nodes) == capacity {
					front := buckets[low].Front()
					oldest := front.Value.(*lfuEntry)
					buckets[low].Remove(front)
					if buckets[low].Len() == 0 {
						delete(buckets, low)
					}
					delete(nodes, oldest.key)
				}
				e := &lfuEntry{key: key, value: value, count: 1}
				nb, ok := buckets[1]
				if !ok {
					nb = list.New()
					buckets[1] = nb
				}
				nodes[key] = nb.PushBack(e)
				low = 1
			}
		}
	}
	return out
}

func main() {
	fmt.Println(runLfu(2, []string{"put 1 1", "put 2 2", "get 1", "put 3 3", "get 2", "get 3", "put 4 4", "get 1", "get 3", "get 4"}))
}
