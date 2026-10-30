package main

import "fmt"

// O(max(len(a), len(b))) time, O(max(len(a), len(b))) space
func addBinary(a string, b string) string {
	var out []byte
	i, j, carry := len(a)-1, len(b)-1, 0
	for i >= 0 || j >= 0 || carry > 0 {
		total := carry
		if i >= 0 {
			total += int(a[i] - '0')
			i--
		}
		if j >= 0 {
			total += int(b[j] - '0')
			j--
		}
		out = append(out, byte('0'+total%2))
		carry = total / 2
	}
	for l, r := 0, len(out)-1; l < r; l, r = l+1, r-1 {
		out[l], out[r] = out[r], out[l]
	}
	return string(out)
}

func main() {
	fmt.Println(addBinary("11", "1"))
}
