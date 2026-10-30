// O(n log C) time, O(1) extra space
fn ship_capacity(weights: Vec<i64>, days: i64) -> i64 {
    let mut lo = *weights.iter().max().unwrap();
    let mut hi: i64 = weights.iter().sum();

    while lo < hi {
        let mid = (lo + hi) / 2;
        let mut needed = 1i64;
        let mut load = 0i64;

        for &w in &weights {
            if load + w > mid {
                needed += 1;
                load = 0;
            }
            load += w;
        }

        if needed <= days {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn main() {
    println!("{:?}", ship_capacity(vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5));
}
