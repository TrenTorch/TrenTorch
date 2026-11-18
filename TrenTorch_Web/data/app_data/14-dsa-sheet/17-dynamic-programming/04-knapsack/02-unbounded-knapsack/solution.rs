fn unbounded_knapsack(weights: Vec<i64>, values: Vec<i64>, capacity: i64) -> i64 {
    // O(n * capacity) time, O(capacity) space
    let cap = capacity as usize;
    let mut best = vec![0i64; cap + 1];
    for (w, v) in weights.iter().zip(values.iter()) {
        let weight = *w as usize;
        let value = *v;
        for w_idx in weight..=cap {
            let candidate = best[w_idx - weight] + value;
            if candidate > best[w_idx] {
                best[w_idx] = candidate;
            }
        }
    }
    best[cap]
}

fn main() {
    println!("{:?}", unbounded_knapsack(vec![1, 3, 4], vec![15, 50, 60], 8));
}
