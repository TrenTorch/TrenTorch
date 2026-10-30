package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
)

// O(n log n * L) time where L is the max digit length, O(n * L) space
func largestNumber(nums []int) string {
	strs := make([]string, len(nums))
	for i, x := range nums {
		strs[i] = strconv.Itoa(x)
	}
	sort.SliceStable(strs, func(i, j int) bool {
		return strs[i]+strs[j] > strs[j]+strs[i]
	})
	result := strings.Join(strs, "")
	if result == "" || result[0] == '0' {
		return "0"
	}
	return result
}

func main() {
	fmt.Println(largestNumber([]int{10, 2}))
}
