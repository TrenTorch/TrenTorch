package main

import "fmt"

// O(n) time, O(1) space (at most three keys live in the map at once)
func totalFruit(fruits []int) int {
	count := make(map[int]int)
	left := 0
	best := 0
	for right, f := range fruits {
		count[f]++
		for len(count) > 2 {
			count[fruits[left]]--
			if count[fruits[left]] == 0 {
				delete(count, fruits[left])
			}
			left++
		}
		if right-left+1 > best {
			best = right - left + 1
		}
	}
	return best
}

func main() {
	fmt.Println(totalFruit([]int{1, 2, 3, 2, 2}))
}
