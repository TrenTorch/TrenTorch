package main

import "fmt"

// O(n^2 log C) time, O(n) space
func maxPoints(points [][]int) int {
	n := len(points)
	if n <= 2 {
		return n
	}
	best := 2
	for i := 0; i < n; i++ {
		slopes := make(map[[2]int]int)
		x0, y0 := points[i][0], points[i][1]
		for j := i + 1; j < n; j++ {
			dx, dy := points[j][0]-x0, points[j][1]-y0
			g := gcd(abs(dx), abs(dy))
			dx, dy = dx/g, dy/g
			if dx < 0 || (dx == 0 && dy < 0) {
				dx, dy = -dx, -dy
			}
			slopes[[2]int{dx, dy}]++
		}
		for _, c := range slopes {
			if c+1 > best {
				best = c + 1
			}
		}
	}
	return best
}

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	fmt.Println(maxPoints([][]int{[]int{1, 1}, []int{2, 2}, []int{3, 3}}))
}
