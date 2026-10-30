package main

import "fmt"

// O(n log log n) time, O(n) space
func countPrimes(n int) int {
	if n < 3 {
		return 0
	}
	sieve := make([]bool, n)
	for i := range sieve {
		sieve[i] = true
	}
	sieve[0] = false
	sieve[1] = false
	for i := 2; i*i <= n; i++ {
		if sieve[i] {
			for j := i * i; j < n; j += i {
				sieve[j] = false
			}
		}
	}
	count := 0
	for _, isPrime := range sieve {
		if isPrime {
			count++
		}
	}
	return count
}

func main() {
	fmt.Println(countPrimes(10))
}
