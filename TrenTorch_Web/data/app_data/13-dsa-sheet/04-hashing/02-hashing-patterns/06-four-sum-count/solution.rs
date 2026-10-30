// O(n^2) time, O(n^2) space
fn four_sum_count(a: Vec<i64>, b: Vec<i64>, c: Vec<i64>, d: Vec<i64>) -> i64 {
    use std::collections::HashMap;
    let mut sum_counts = HashMap::new();
    for x in &a {
        for y in &b {
            *sum_counts.entry(x + y).or_insert(0) += 1;
        }
    }
    let mut total = 0;
    for z in &c {
        for w in &d {
            let target = -(z + w);
            if let Some(&cnt) = sum_counts.get(&target) {
                total += cnt;
            }
        }
    }
    total
}

fn main() {
    println!("{:?}", four_sum_count(vec![1, 2], vec![-2, -1], vec![-1, 2], vec![0, 2]));
}
