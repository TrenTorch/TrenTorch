package main

import "fmt"

// O(N * alpha(N)) time, O(N) space, N = number of stones
func removeStones(stones [][]int) int {
	parent := map[int]int{}
	size := map[int]int{}
	find := func(a int) int {
		if _, ok := parent[a]; !ok {
			parent[a] = a
			size[a] = 1
		}
		for parent[a] != a {
			parent[a] = parent[parent[a]]
			a = parent[a]
		}
		return a
	}
	for _, s := range stones {
		x, y := s[0], s[1]
		ra, rb := find(x), find(y+10001)
		if ra != rb {
			if size[ra] < size[rb] {
				ra, rb = rb, ra
			}
			parent[rb] = ra
			size[ra] += size[rb]
		}
	}
	groups := map[int]bool{}
	for _, s := range stones {
		groups[find(s[0])] = true
	}
	return len(stones) - len(groups)
}

func main() {
	fmt.Println(removeStones([][]int{[]int{0, 0}, []int{0, 1}, []int{1, 0}, []int{1, 2}, []int{2, 1}, []int{2, 2}}))
}
