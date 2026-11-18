// O(n log n) time, O(1) auxiliary space
fn fractional_knapsack(items: Vec<Vec<i64>>, capacity: i64) -> f64 {
    let mut items = items;
    items.sort_by(|a, b| {
        let v1 = a[0];
        let w1 = a[1];
        let v2 = b[0];
        let w2 = b[1];
        // Compare v2/w2 vs v1/w1 for descending order
        // v1/w1 > v2/w2  <=> v1 * w2 > v2 * w1
        (v2 * w1).cmp(&(v1 * w2))
    });
    let mut total = 0.0;
    let mut cap = capacity;
    for item in items {
        if cap == 0 {
            break;
        }
        let value = item[0] as f64;
        let weight = item[1];
        let take = weight.min(cap);
        total += value * (take as f64) / (weight as f64);
        cap -= take;
    }
    total
}

fn main() {
    println!("{:?}", fractional_knapsack(vec![vec![60, 10], vec![100, 20], vec![120, 30]], 50));
}
