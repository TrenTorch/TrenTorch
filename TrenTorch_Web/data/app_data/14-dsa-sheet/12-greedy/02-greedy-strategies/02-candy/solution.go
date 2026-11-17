package main

import "fmt"

// O(n) time, O(1) space
func candy(ratings []int) int {
	n := len(ratings)
	if n == 0 {
		return 0
	}
	total := 1
	up, down, peak := 0, 0, 0
	for i := 1; i < n; i++ {
		if ratings[i] > ratings[i-1] {
			up++
			down = 0
			peak = up
			total += 1 + up
		} else if ratings[i] == ratings[i-1] {
			up, down, peak = 0, 0, 0
			total++
		} else {
			up = 0
			down++
			total += 1 + down
			if peak >= down {
				total--
			}
		}
	}
	return total
}

func main() {
	fmt.Println(candy([]int{1, 0, 2}))
}
