package main

import "fmt"

// O(len(strs) * m * n) time, O(m * n) space
func findMaxForm(strs []string, m int, n int) int {
	best := make([][]int, m+1)
	for i := range best {
		best[i] = make([]int, n+1)
	}
	for _, s := range strs {
		zeros := 0
		for i := 0; i < len(s); i++ {
			if s[i] == '0' {
				zeros++
			}
		}
		ones := len(s) - zeros
		for z := m; z >= zeros; z-- {
			row := best[z]
			source := best[z-zeros]
			for o := n; o >= ones; o-- {
				if source[o-ones]+1 > row[o] {
					row[o] = source[o-ones] + 1
				}
			}
		}
	}
	return best[m][n]
}

func main() {
	fmt.Println(findMaxForm([]string{"10", "0001", "111001", "1", "0"}, 5, 3))
}
