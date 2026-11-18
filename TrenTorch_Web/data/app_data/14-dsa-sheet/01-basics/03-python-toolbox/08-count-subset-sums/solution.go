package main

import "fmt"

type subsetState struct {
	size  int
	total int
}

// sumsBySize maps (size, sum) to the number of subsets of values with that size and sum.
func sumsBySize(values []int) map[subsetState]int {
	states := map[subsetState]int{{0, 0}: 1}
	for _, v := range values {
		snapshot := make([]subsetState, 0, len(states))
		ways := make([]int, 0, len(states))
		for key, w := range states {
			snapshot = append(snapshot, key)
			ways = append(ways, w)
		}
		for i, key := range snapshot {
			states[subsetState{key.size + 1, key.total + v}] += ways[i]
		}
	}
	return states
}

// O(2^(n/2)) time and space in the worst case (meet in the middle over two halves).
func countSubsetSums(nums []int, k int, target int) int {
	half := len(nums) / 2
	left := sumsBySize(nums[:half])
	right := sumsBySize(nums[half:])
	count := 0
	for key, ways := range right {
		count += ways * left[subsetState{k - key.size, target - key.total}]
	}
	return count
}

func main() {
	fmt.Println(countSubsetSums([]int{1, 2, 3, 4}, 2, 5))
}
