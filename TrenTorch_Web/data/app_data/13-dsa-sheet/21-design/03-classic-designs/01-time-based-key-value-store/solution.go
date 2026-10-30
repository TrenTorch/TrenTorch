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

// O(log n) time per get, O(total sets) space
func runTimeMap(ops []string) []string {
	times := make(map[string][]int)
	values := make(map[string][]string)
	out := []string{}
	for _, op := range ops {
		parts := strings.Fields(op)
		if parts[0] == "set" {
			times[parts[1]] = append(times[parts[1]], mustAtoi(parts[3]))
			values[parts[1]] = append(values[parts[1]], parts[2])
		} else {
			key := parts[1]
			ts := times[key]
			want := mustAtoi(parts[2])
			i := sort.Search(len(ts), func(j int) bool { return ts[j] > want })
			if i > 0 {
				out = append(out, values[key][i-1])
			} else {
				out = append(out, "")
			}
		}
	}
	return out
}

func main() {
	fmt.Println(runTimeMap([]string{"set love high 10", "get love 10", "get love 15", "set love low 20", "get love 15", "get love 25", "get love 5"}))
}
