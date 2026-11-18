// O(n log S) time, O(1) extra space where S is the sum of pages
fn allocate_books(pages: Vec<i64>, students: i64) -> i64 {
    let n = pages.len() as i64;
    if students > n {
        return -1;
    }
    let mut lo = *pages.iter().max().unwrap();
    let mut hi: i64 = pages.iter().sum();
    while lo < hi {
        let mid = (lo + hi) / 2;
        let mut needed = 1i64;
        let mut load = 0i64;
        for &p in &pages {
            if load + p > mid {
                needed += 1;
                load = 0;
            }
            load += p;
        }
        if needed <= students {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn main() {
    println!("{:?}", allocate_books(vec![12, 34, 67, 90], 2));
}
