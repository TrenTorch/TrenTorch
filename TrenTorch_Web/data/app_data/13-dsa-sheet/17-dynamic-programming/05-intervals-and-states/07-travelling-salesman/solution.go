package main

import "fmt"

// O(2^n * n^2) time, O(2^n * n) space
func tsp(dist [][]int) int {
	n := len(dist)
	if n <= 1 {
		return 0
	}
	inf := int(^uint(0) >> 1)
	full := (1 << n) - 1
	best := make([][]int, 1<<n)
	for m := range best {
		best[m] = make([]int, n)
		for j := range best[m] {
			best[m][j] = inf
		}
	}
	best[1][0] = 0
	for mask := 1; mask < 1<<n; mask++ {
		if mask&1 == 0 {
			continue
		}
		for last := 0; last < n; last++ {
			cost := best[mask][last]
			if cost == inf {
				continue
			}
			for nxt := 0; nxt < n; nxt++ {
				if (mask>>nxt)&1 == 0 {
					newMask := mask | (1 << nxt)
					value := cost + dist[last][nxt]
					if value < best[newMask][nxt] {
						best[newMask][nxt] = value
					}
				}
			}
		}
	}
	res := inf
	for last := 1; last < n; last++ {
		if best[full][last] == inf {
			continue
		}
		res = min(res, best[full][last]+dist[last][0])
	}
	return res
}

func main() {
	fmt.Println(tsp([][]int{[]int{0, 10, 15, 20}, []int{10, 0, 35, 25}, []int{15, 35, 0, 30}, []int{20, 25, 30, 0}}))
}
