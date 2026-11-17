package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
)

func mustAtoi(s string) int {
	v, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return v
}

// O(log s) time per get, O(number of changes) space
func runSnapshotArray(length int, ops []string) []int {
	ids := make(map[int][]int)
	vals := make(map[int][]int)
	snapID := 0
	out := []int{}
	for _, op := range ops {
		parts := strings.Fields(op)
		switch parts[0] {
		case "set":
			i, v := mustAtoi(parts[1]), mustAtoi(parts[2])
			l := ids[i]
			if len(l) > 0 && l[len(l)-1] == snapID {
				vals[i][len(vals[i])-1] = v
			} else {
				ids[i] = append(ids[i], snapID)
				vals[i] = append(vals[i], v)
			}
		case "snap":
			out = append(out, snapID)
			snapID++
		default:
			i, want := mustAtoi(parts[1]), mustAtoi(parts[2])
			l := ids[i]
			k := sort.Search(len(l), func(j int) bool { return l[j] > want }) - 1
			if k >= 0 {
				out = append(out, vals[i][k])
			} else {
				out = append(out, 0)
			}
		}
	}
	return out
}

func main() {
	fmt.Println(runSnapshotArray(3, []string{"set 0 5", "snap", "set 0 6", "get 0 0", "snap", "get 0 1"}))
}
