package main

import "fmt"

// O(4^n * n) time, O(n) extra space beyond the output
func letterCombinations(digits string) []string {
	keys := map[byte]string{
		'2': "abc",
		'3': "def",
		'4': "ghi",
		'5': "jkl",
		'6': "mno",
		'7': "pqrs",
		'8': "tuv",
		'9': "wxyz",
	}
	if len(digits) == 0 {
		return []string{}
	}
	out := []string{}
	var buf []byte
	var rec func(i int)
	rec = func(i int) {
		if i == len(digits) {
			out = append(out, string(buf))
			return
		}
		for _, letter := range []byte(keys[digits[i]]) {
			buf = append(buf, letter)
			rec(i + 1)
			buf = buf[:len(buf)-1]
		}
	}
	rec(0)
	return out
}

func main() {
	fmt.Println(letterCombinations("23"))
}
