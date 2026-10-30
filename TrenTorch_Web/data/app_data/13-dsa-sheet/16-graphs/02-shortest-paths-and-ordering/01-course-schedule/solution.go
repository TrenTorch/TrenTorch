package main

import "fmt"

// O(V + E) time, O(V + E) space
func canFinish(numCourses int, prerequisites [][]int) bool {
	adj := make([][]int, numCourses)
	inDegree := make([]int, numCourses)
	for _, p := range prerequisites {
		course, pre := p[0], p[1]
		adj[pre] = append(adj[pre], course)
		inDegree[course]++
	}
	queue := []int{}
	for v := 0; v < numCourses; v++ {
		if inDegree[v] == 0 {
			queue = append(queue, v)
		}
	}
	taken := 0
	for head := 0; head < len(queue); head++ {
		node := queue[head]
		taken++
		for _, nxt := range adj[node] {
			inDegree[nxt]--
			if inDegree[nxt] == 0 {
				queue = append(queue, nxt)
			}
		}
	}
	return taken == numCourses
}

func main() {
	fmt.Println(canFinish(2, [][]int{[]int{1, 0}}))
}
