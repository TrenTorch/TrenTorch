package main

import "fmt"

// O(eggs * answer) time, O(eggs) space
func eggDrop(eggs int, floors int) int {
	if floors == 0 || eggs == 0 {
		return 0
	}
	reach := make([]int, eggs+1)
	drops := 0
	for reach[eggs] < floors {
		drops++
		for e := eggs; e > 0; e-- {
			reach[e] = reach[e-1] + reach[e] + 1
		}
	}
	return drops
}

func main() {
	fmt.Println(eggDrop(2, 6))
}
