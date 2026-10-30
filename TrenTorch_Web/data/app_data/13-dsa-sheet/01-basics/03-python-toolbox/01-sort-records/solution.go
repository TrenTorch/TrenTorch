package main

import (
	"fmt"
	"sort"
)

// Record is one [name, score] entry.
type Record struct {
	Name  string
	Score int
}

// O(n log n) time, O(n) space
func sortRecords(records []Record) []string {
	sorted := make([]Record, len(records))
	copy(sorted, records)
	sort.Slice(sorted, func(i, j int) bool {
		if sorted[i].Score != sorted[j].Score {
			return sorted[i].Score > sorted[j].Score
		}
		return sorted[i].Name < sorted[j].Name
	})
	names := make([]string, 0, len(sorted))
	for _, r := range sorted {
		names = append(names, r.Name)
	}
	return names
}

func main() {
	fmt.Println(sortRecords([]Record{{"bo", 5}, {"al", 9}, {"cy", 5}}))
}
