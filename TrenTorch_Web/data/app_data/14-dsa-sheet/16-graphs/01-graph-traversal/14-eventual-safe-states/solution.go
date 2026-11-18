package main

import "fmt"

// O(n + E) time, O(n + E) space
func eventualSafeNodes(n int, edges [][]int) []int {
	rev := make([][]int, n)
	outDegree := make([]int, n)
	for _, e := range edges {
		a, b := e[0], e[1]
		rev[b] = append(rev[b], a)
		outDegree[a]++
	}
	queue := []int{}
	for v := 0; v < n; v++ {
		if outDegree[v] == 0 {
			queue = append(queue, v)
		}
	}
	safe := make([]bool, n)
	for head := 0; head < len(queue); head++ {
		node := queue[head]
		safe[node] = true
		for _, p := range rev[node] {
			outDegree[p]--
			if outDegree[p] == 0 {
				queue = append(queue, p)
			}
		}
	}
	result := []int{}
	for v := 0; v < n; v++ {
		if safe[v] {
			result = append(result, v)
		}
	}
	return result
}

func main() {
	fmt.Println(eventualSafeNodes(7, [][]int{[]int{0, 1}, []int{0, 2}, []int{1, 2}, []int{1, 3}, []int{2, 5}, []int{3, 0}, []int{4, 5}}))
}
