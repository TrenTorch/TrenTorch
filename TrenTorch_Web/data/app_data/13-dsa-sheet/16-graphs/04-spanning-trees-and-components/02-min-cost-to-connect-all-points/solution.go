package main

import "fmt"

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

// O(n^2) time, O(n) space
func minCostConnectPoints(points [][]int) int {
	n := len(points)
	if n == 0 {
		return 0
	}
	const inf = int(^uint(0) >> 1)
	best := make([]int, n)
	for i := range best {
		best[i] = inf
	}
	best[0] = 0
	used := make([]bool, n)
	total := 0
	for iter := 0; iter < n; iter++ {
		u := -1
		for v := 0; v < n; v++ {
			if !used[v] && (u == -1 || best[v] < best[u]) {
				u = v
			}
		}
		used[u] = true
		total += best[u]
		ux, uy := points[u][0], points[u][1]
		for v := 0; v < n; v++ {
			if !used[v] {
				dist := abs(points[v][0]-ux) + abs(points[v][1]-uy)
				if dist < best[v] {
					best[v] = dist
				}
			}
		}
	}
	return total
}

func main() {
	fmt.Println(minCostConnectPoints([][]int{[]int{0, 0}, []int{2, 2}, []int{3, 10}, []int{5, 2}, []int{7, 0}}))
}
