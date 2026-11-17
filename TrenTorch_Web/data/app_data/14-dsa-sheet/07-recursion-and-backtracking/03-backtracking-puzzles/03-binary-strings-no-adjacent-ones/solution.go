package main

import "fmt"

// O(F(n) * n) time where F(n) is the answer count (~1.6^n), O(n) extra space
func noAdjacentOnes(n int) []string {
	out := []string{}
	buf := make([]byte, 0, n)
	var rec func()
	rec = func() {
		if len(buf) == n {
			out = append(out, string(buf))
			return
		}
		buf = append(buf, '0')
		rec()
		buf = buf[:len(buf)-1]
		if len(buf) == 0 || buf[len(buf)-1] != '1' {
			buf = append(buf, '1')
			rec()
			buf = buf[:len(buf)-1]
		}
	}
	rec()
	return out
}

func main() {
	fmt.Println(noAdjacentOnes(3))
}
