package main

import (
	"container/list"
	"fmt"
	"strconv"
	"strings"
)

type lruEntry struct {
	key, value int
}

func mustAtoi(s string) int {
	v, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return v
}

// O(1) time per operation, O(capacity) space
func runLru(capacity int, ops []string) []int {
	cache := make(map[int]*list.Element)
	ll := list.New()
	out := []int{}
	for _, op := range ops {
		parts := strings.Fields(op)
		if parts[0] == "get" {
			key := mustAtoi(parts[1])
			if el, ok := cache[key]; ok {
				ll.MoveToFront(el)
				out = append(out, el.Value.(*lruEntry).value)
			} else {
				out = append(out, -1)
			}
		} else if capacity > 0 {
			key, value := mustAtoi(parts[1]), mustAtoi(parts[2])
			if el, ok := cache[key]; ok {
				ll.MoveToFront(el)
				el.Value.(*lruEntry).value = value
			} else {
				if ll.Len() == capacity {
					back := ll.Back()
					ll.Remove(back)
					delete(cache, back.Value.(*lruEntry).key)
				}
				cache[key] = ll.PushFront(&lruEntry{key: key, value: value})
			}
		}
	}
	return out
}

func main() {
	fmt.Println(runLru(2, []string{"put 1 1", "put 2 2", "get 1", "put 3 3", "get 2", "put 4 4", "get 1", "get 3", "get 4"}))
}
