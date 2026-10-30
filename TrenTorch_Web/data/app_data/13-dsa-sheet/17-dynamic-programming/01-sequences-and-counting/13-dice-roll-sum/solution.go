package main

import "fmt"

// O(dice * target) time, O(target) space
func diceWays(dice int, faces int, target int) int {
	const mod = 1000000007
	row := make([]int, target+1)
	row[0] = 1
	for d := 0; d < dice; d++ {
		prefix := make([]int, target+2)
		for t := 0; t <= target; t++ {
			prefix[t+1] = (prefix[t] + row[t]) % mod
		}
		nxt := make([]int, target+1)
		for t := 1; t <= target; t++ {
			lo := t - faces
			if lo < 0 {
				lo = 0
			}
			nxt[t] = ((prefix[t]-prefix[lo])%mod + mod) % mod
		}
		row = nxt
	}
	return row[target]
}

func main() {
	fmt.Println(diceWays(2, 6, 7))
}
