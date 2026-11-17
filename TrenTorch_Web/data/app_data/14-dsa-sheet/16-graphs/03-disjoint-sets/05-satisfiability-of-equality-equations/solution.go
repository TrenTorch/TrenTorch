package main

import "fmt"

// O(E * alpha(26)) time, O(1) space
func equationsPossible(equations []string) bool {
	parent := make([]int, 26)
	for i := range parent {
		parent[i] = i
	}
	find := func(a int) int {
		for parent[a] != a {
			parent[a] = parent[parent[a]]
			a = parent[a]
		}
		return a
	}
	for _, eq := range equations {
		if eq[1] == '=' {
			ra := find(int(eq[0] - 'a'))
			rb := find(int(eq[3] - 'a'))
			parent[ra] = rb
		}
	}
	for _, eq := range equations {
		if eq[1] == '!' && find(int(eq[0]-'a')) == find(int(eq[3]-'a')) {
			return false
		}
	}
	return true
}

func main() {
	fmt.Println(equationsPossible([]string{"a==b", "b!=a"}))
}
