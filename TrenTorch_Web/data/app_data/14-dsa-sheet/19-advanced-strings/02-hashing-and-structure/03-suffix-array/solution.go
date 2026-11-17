package main

import "fmt"

// O(n log n) time, O(n) space
func suffixArray(s string) []int {
	if len(s) == 0 {
		return []int{}
	}
	n := len(s) + 1
	text := make([]int, n)
	maxV := 0
	for i := 0; i < len(s); i++ {
		text[i] = int(s[i]) + 1
		if text[i] > maxV {
			maxV = text[i]
		}
	}
	text[n-1] = 0 // sentinel, smaller than every letter

	size := maxV + 1
	if n > size {
		size = n
	}
	order := make([]int, n)
	cls := make([]int, n)
	count := make([]int, size)
	for _, v := range text {
		count[v]++
	}
	for i := 1; i < size; i++ {
		count[i] += count[i-1]
	}
	for i := n - 1; i >= 0; i-- {
		count[text[i]]--
		order[count[text[i]]] = i
	}
	classes := 1
	for i := 1; i < n; i++ {
		if text[order[i]] != text[order[i-1]] {
			classes++
		}
		cls[order[i]] = classes - 1
	}

	for shift := 1; shift < n; shift *= 2 {
		bySecond := make([]int, n)
		for i, o := range order {
			bySecond[i] = ((o-shift)%n + n) % n
		}
		count = make([]int, classes)
		for i := 0; i < n; i++ {
			count[cls[bySecond[i]]]++
		}
		for i := 1; i < classes; i++ {
			count[i] += count[i-1]
		}
		for i := n - 1; i >= 0; i-- {
			c := cls[bySecond[i]]
			count[c]--
			order[count[c]] = bySecond[i]
		}
		newCls := make([]int, n)
		classes = 1
		for i := 1; i < n; i++ {
			a, b := order[i], order[i-1]
			if cls[a] != cls[b] || cls[(a+shift)%n] != cls[(b+shift)%n] {
				classes++
			}
			newCls[a] = classes - 1
		}
		newCls[order[0]] = 0
		cls = newCls
	}
	return order[1:]
}

func main() {
	fmt.Println(suffixArray("banana"))
}
