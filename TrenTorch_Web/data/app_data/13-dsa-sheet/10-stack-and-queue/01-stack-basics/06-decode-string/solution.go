package main

import "fmt"

type openBlock struct {
	start int
	count int
}

// O(L) time and O(L) space, where L is the decoded length.
func decodeString(s string) string {
	out := []byte{}
	openBlocks := []openBlock{}
	num := 0
	for i := 0; i < len(s); i++ {
		ch := s[i]
		if ch >= '0' && ch <= '9' {
			num = num*10 + int(ch-'0')
		} else if ch == '[' {
			openBlocks = append(openBlocks, openBlock{start: len(out), count: num})
			num = 0
		} else if ch == ']' {
			b := openBlocks[len(openBlocks)-1]
			openBlocks = openBlocks[:len(openBlocks)-1]
			if b.count == 0 {
				out = out[:b.start]
			} else if b.count > 1 {
				segment := append([]byte(nil), out[b.start:]...)
				for k := 1; k < b.count; k++ {
					out = append(out, segment...)
				}
			}
		} else {
			out = append(out, ch)
		}
	}
	return string(out)
}

func main() {
	fmt.Println(decodeString("3[a2[c]]"))
}
