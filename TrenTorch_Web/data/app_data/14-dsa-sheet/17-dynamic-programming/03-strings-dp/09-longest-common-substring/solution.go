package main

import "fmt"

// O(|a|) states/transitions for the suffix automaton of a, O(|b|) scan of b
func longestCommonSubstring(a string, b string) int {
	// suffix automaton of a
	nxt := []map[byte]int{make(map[byte]int)}
	link := []int{-1}
	length := []int{0}
	last := 0
	for i := 0; i < len(a); i++ {
		ch := a[i]
		cur := len(nxt)
		nxt = append(nxt, make(map[byte]int))
		length = append(length, length[last]+1)
		link = append(link, 0)
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
				copied := make(map[byte]int, len(nxt[q]))
				for k, v := range nxt[q] {
					copied[k] = v
				}
				nxt = append(nxt, copied)
				length = append(length, length[p]+1)
				link = append(link, link[q])
				for p != -1 {
					if v, ok := nxt[p][ch]; !ok || v != q {
						break
					}
					nxt[p][ch] = clone
					p = link[p]
				}
				link[q] = clone
				link[cur] = clone
			}
		}
		last = cur
	}

	best, match, state := 0, 0, 0
	for i := 0; i < len(b); i++ {
		ch := b[i]
		for state != 0 {
			if _, ok := nxt[state][ch]; ok {
				break
			}
			state = link[state]
			match = length[state]
		}
		if v, ok := nxt[state][ch]; ok {
			state = v
			match++
		} else {
			state = 0
			match = 0
		}
		if match > best {
			best = match
		}
	}
	return best
}

func main() {
	fmt.Println(longestCommonSubstring("abcdxyz", "xyzabcd"))
}
