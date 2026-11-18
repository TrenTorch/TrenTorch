// O(n log D) time, O(1) extra space where D is the range of bloom days
fn min_days_bouquets(bloom: Vec<i64>, m: i64, k: i64) -> i64 {
    let n = bloom.len() as i64;
    if m * k > n {
        return -1;
    }

    fn possible(bloom: &Vec<i64>, day: i64, m: i64, k: i64) -> bool {
        let mut bouquets = 0i64;
        let mut run = 0i64;
        for &b in bloom.iter() {
            if b <= day {
                run += 1;
                if run == k {
                    bouquets += 1;
                    if bouquets >= m {
                        return true;
                    }
                    run = 0;
                }
            } else {
                run = 0;
            }
        }
        bouquets >= m
    }

    let mut lo = *bloom.iter().min().unwrap();
    let mut hi = *bloom.iter().max().unwrap();
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if possible(&bloom, mid, m, k) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn main() {
    println!("{:?}", min_days_bouquets(vec![1, 10, 3, 10, 2], 3, 1));
}
