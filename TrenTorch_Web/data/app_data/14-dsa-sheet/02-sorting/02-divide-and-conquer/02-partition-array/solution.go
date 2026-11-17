package main

// O(n) time, O(n) space for the copy (Lomuto partition with the last value as pivot).
func partitionArray(nums []int) ([]int, int) {
	a := append([]int(nil), nums...)
	pivot := a[len(a)-1]
	i := -1
	for j := 0; j < len(a)-1; j++ {
		if a[j] <= pivot {
			i++
			a[i], a[j] = a[j], a[i]
		}
	}
	a[i+1], a[len(a)-1] = a[len(a)-1], a[i+1]
	return a, i + 1
}

func main() {
}
