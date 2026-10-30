// O(log n) time, O(1) space
fn nth_root(n: i64, m: i64) -> i64 {
    let bit_len = 64 - n.leading_zeros();
    let hi = 1i64 << (bit_len / m as u32 + 1);
    let mut lo = 1i64;
    let mut hi = hi;
    while lo <= hi {
        let mid = (lo + hi) / 2;
        let power = pow_with_limit(mid, m, n);
        if power == n {
            return mid;
        }
        if power < n {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    -1
}

fn pow_with_limit(base: i64, exp: i64, limit: i64) -> i64 {
    let mut result = 1i64;
    for _ in 0..exp {
        result = match result.checked_mul(base) {
            Some(v) if v <= limit => v,
            _ => return limit + 1,
        };
    }
    result
}

fn main() {
    println!("{:?}", nth_root(27, 3));
}
