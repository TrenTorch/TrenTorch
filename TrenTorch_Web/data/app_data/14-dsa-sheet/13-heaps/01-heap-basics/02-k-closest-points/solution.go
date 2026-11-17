package main

import (
	"fmt"
	"math/rand"
	"sort"
)

type closestItem struct {
	key [3]int // (squared distance, x, y)
	p   []int
}

// lessKey compares keys like Python tuple comparison
func lessKey(a, b [3]int) bool {
	for i := 0; i < 3; i++ {
		if a[i] != b[i] {
			return a[i] < b[i]
		}
	}
	return false
}

// O(n) expected time for quickselect plus O(k log k) final sort, O(n) space
func kClosest(points [][]int, k int) [][]int {
	if k <= 0 {
		return [][]int{}
	}
	pool := make([]closestItem, 0, len(points))
	for _, p := range points {
		pool = append(pool, closestItem{key: [3]int{p[0]*p[0] + p[1]*p[1], p[0], p[1]}, p: p})
	}
	if k < len(pool) {
		var chosen []closestItem
		need := k
		for need > 0 {
			pivot := pool[rand.Intn(len(pool))].key
			var less, equal []closestItem
			for _, item := range pool {
				if lessKey(item.key, pivot) {
					less = append(less, item)
				} else if item.key == pivot {
					equal = append(equal, item)
				}
			}
			if need <= len(less) {
				pool = less
			} else if need <= len(less)+len(equal) {
				chosen = append(chosen, less...)
				chosen = append(chosen, equal[:need-len(less)]...)
				need = 0
			} else {
				chosen = append(chosen, less...)
				chosen = append(chosen, equal...)
				need -= len(less) + len(equal)
				var greater []closestItem
				for _, item := range pool {
					if lessKey(pivot, item.key) {
						greater = append(greater, item)
					}
				}
				pool = greater
			}
		}
		pool = chosen
	}
	sort.SliceStable(pool, func(i, j int) bool {
		return lessKey(pool[i].key, pool[j].key)
	})
	out := make([][]int, len(pool))
	for i, item := range pool {
		out[i] = item.p
	}
	return out
}

func main() {
	fmt.Println(kClosest([][]int{[]int{1, 3}, []int{-2, 2}}, 1))
}
