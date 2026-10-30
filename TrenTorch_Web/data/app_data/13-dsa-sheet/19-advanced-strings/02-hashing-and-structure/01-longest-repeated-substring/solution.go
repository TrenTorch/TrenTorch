package main

import "fmt"

// O(n * sigma) time and space with sigma the alphabet size (suffix automaton)
func longestRepeatedLength(s string) int {
	nxt := []map[byte]int{{}}
	link := []int{-1}
	length := []int{0}
	occ := []int{0}
	last := 0
	for i := 0; i < len(s); i++ {
		ch := s[i]
		cur := len(nxt)
		nxt = append(nxt, map[byte]int{})
		link = append(link, 0)
		length = append(length, length[last]+1)
		occ = append(occ, 1)
		p := last
		for p != -1 {
			if _, ok := nxt[p][ch]; ok {
				break
			}
			nxt[p][ch] = cur
			p = link[p]
		}
		if p != -1 {
			q := nxt[p][ch]
			if length[p]+1 == length[q] {
				link[cur] = q
			} else {
				clone := len(nxt)
				m := make(map[byte]int, len(nxt[q]))
				for key, val := range nxt[q] {
					m[key] = val
				}
				nxt = append(nxt, m)
				link = append(link, link[q])
				length = append(length, length[p]+1)
				occ = append(occ, 0)
				for p != -1 && nxt[p][ch] == q {
					nxt[p][ch] = clone
					p = link[p]
				}
				link[q] = clone
				link[cur] = clone
			}
		}
		last = cur
	}

	n := len(s)
	byLength := make([][]int, n+1)
	for v := 1; v < len(nxt); v++ {
		byLength[length[v]] = append(byLength[length[v]], v)
	}
	best := 0
	for size := n; size >= 1; size-- {
		for _, v := range byLength[size] {
			if occ[v] >= 2 && size > best {
				best = size
			}
			occ[link[v]] += occ[v]
		}
	}
	return best
}

func main() {
	fmt.Println(longestRepeatedLength("banana"))
}
