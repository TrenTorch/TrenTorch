// O(n * log(max pile)) time, O(1) space
fn min_eating_speed(piles: Vec<i64>, hours: i64) -> i64 {
    let mut lo: i64 = 1;
    let mut hi: i64 = *piles.iter().max().unwrap_or(&1);
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        let needed: i64 = piles.iter().map(|&p| (p + mid - 1) / mid).sum();
        if needed <= hours {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn main() {
    println!("{:?}", min_eating_speed(vec![3, 6, 7, 11], 8));
}
