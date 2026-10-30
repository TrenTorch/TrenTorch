package main

import (
	"fmt"
	"sort"
	"strings"
)

// O(1) time for fixed-size search (at most 3^3 splits), O(1) extra space beyond output
func restoreIpAddresses(s string) []string {
	out := []string{}
	valid := func(part string) bool {
		if len(part) > 1 && part[0] == '0' {
			return false
		}
		v := 0
		for i := 0; i < len(part); i++ {
			v = v*10 + int(part[i]-'0')
		}
		return v <= 255
	}
	parts := make([]string, 0, 4)
	var rec func(start int)
	rec = func(start int) {
		if len(parts) == 4 {
			if start == len(s) {
				out = append(out, strings.Join(parts, "."))
			}
			return
		}
		for length := 1; length <= 3; length++ {
			if start+length > len(s) {
				break
			}
			part := s[start : start+length]
			if valid(part) {
				parts = append(parts, part)
				rec(start + length)
				parts = parts[:len(parts)-1]
			}
		}
	}
	rec(0)
	sort.Strings(out)
	return out
}

func main() {
	fmt.Println(restoreIpAddresses("25525511135"))
}
