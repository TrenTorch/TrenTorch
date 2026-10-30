package main

import (
	"fmt"
	"math/rand"
	"sort"
)

// lessPair orders (-count, value) pairs
func lessPair(a, b [2]int) bool {
	if a[0] != b[0] {
		return a[0] < b[0]
	}
	return a[1] < b[1]
}

// O(d) expected time with randomized quickselect (d = distinct values), O(d) space
func topKFrequent(nums []int, k int) []int {
	counts := map[int]int{}
	for _, x := range nums {
		counts[x]++
	}
	pairs := make([][2]int, 0, len(counts))
	for v, c := range counts {
		pairs = append(pairs, [2]int{-c, v})
	}
	if k <= 0 {
		return []int{}
	}
	if k < len(pairs) {
		chosen := [][2]int{}
		pool := pairs
		need := k
		for need > 0 {
			pivot := pool[rand.Intn(len(pool))]
			less := [][2]int{}
			for _, p := range pool {
				if lessPair(p, pivot) {
					less = append(less, p)
				}
			}
			if need <= len(less) {
				pool = less
			} else if need == len(less)+1 {
				chosen = append(chosen, less...)
				chosen = append(chosen, pivot)
				need = 0
			} else {
				chosen = append(chosen, less...)
				chosen = append(chosen, pivot)
				need -= len(less) + 1
				greater := [][2]int{}
				for _, p := range pool {
					if lessPair(pivot, p) {
						greater = append(greater, p)
					}
				}
				pool = greater
			}
		}
		pairs = chosen
	}
	sort.Slice(pairs, func(i, j int) bool { return lessPair(pairs[i], pairs[j]) })
	out := make([]int, len(pairs))
	for i, p := range pairs {
		out[i] = p[1]
	}
	return out
}

func main() {
	fmt.Println(topKFrequent([]int{1, 1, 1, 2, 2, 3}, 2))
}
