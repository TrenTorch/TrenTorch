package main

import "fmt"

// O(n^3) time, O(n^2) space
func allPairsShortest(n int, edges [][]int) [][]int {
	const inf = int(^uint(0) >> 1)
	dist := make([][]int, n)
	for i := range dist {
		dist[i] = make([]int, n)
		for j := range dist[i] {
			dist[i][j] = inf
		}
	}
	for i := 0; i < n; i++ {
		dist[i][i] = 0
	}
	for _, e := range edges {
		a, b, w := e[0], e[1], e[2]
		if w < dist[a][b] {
			dist[a][b] = w
		}
	}
	for k := 0; k < n; k++ {
		rowK := dist[k]
		for i := 0; i < n; i++ {
			dik := dist[i][k]
			if dik == inf {
				continue
			}
			rowI := dist[i]
			for j := 0; j < n; j++ {
				if rowK[j] == inf {
					continue
				}
				if dik+rowK[j] < rowI[j] {
					rowI[j] = dik + rowK[j]
				}
			}
		}
	}
	for i := range dist {
		for j := range dist[i] {
			if dist[i][j] == inf {
				dist[i][j] = -1
			}
		}
	}
	return dist
}

func main() {
	fmt.Println(allPairsShortest(3, [][]int{[]int{0, 1, 4}, []int{1, 2, 1}, []int{0, 2, 7}}))
}
