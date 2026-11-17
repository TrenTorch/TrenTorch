// O(items * capacity) time, O(capacity) space
fn knapsack(weights: Vec<i64>, values: Vec<i64>, capacity: i64) -> i64 {
    let cap = capacity as usize;
    let mut best = vec![0i64; cap + 1];
    for (&weight, &value) in weights.iter().zip(values.iter()) {
        let wt = weight as usize;
        for w in (wt..=cap).rev() {
            let candidate = best[w - wt] + value;
            if candidate > best[w] {
                best[w] = candidate;
            }
        }
    }
    best[cap]
}

fn main() {
    println!("{:?}", knapsack(vec![1, 3, 4, 5], vec![1, 4, 5, 7], 7));
}
