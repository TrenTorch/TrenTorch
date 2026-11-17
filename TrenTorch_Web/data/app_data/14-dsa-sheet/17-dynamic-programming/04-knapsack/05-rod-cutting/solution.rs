// O(n^2) time, O(n) space where n = length
fn rod_cutting(prices: Vec<i64>, length: i64) -> i64 {
    let n = length as usize;
    let mut best = vec![0; n + 1];
    for i in 1..=n {
        let mut max_val = 0;
        for k in 1..=i {
            let val = prices[k - 1] + best[i - k];
            if val > max_val {
                max_val = val;
            }
        }
        best[i] = max_val;
    }
    best[n]
}

fn main() {
    println!("{:?}", rod_cutting(vec![1, 5, 8, 9, 10, 17, 17, 20], 8));
}
