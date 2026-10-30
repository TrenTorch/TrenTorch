package main

import "fmt"

// O(n) time, O(1) space
func lemonadeChange(bills []int) bool {
	fives, tens := 0, 0
	for _, bill := range bills {
		switch bill {
		case 5:
			fives++
		case 10:
			if fives == 0 {
				return false
			}
			fives--
			tens++
		default:
			if tens > 0 && fives > 0 {
				tens--
				fives--
			} else if fives >= 3 {
				fives -= 3
			} else {
				return false
			}
		}
	}
	return true
}

func main() {
	fmt.Println(lemonadeChange([]int{5, 5, 5, 10, 20}))
}
