fn cost(growth: &str, n: i64) -> u128 {
    match growth {
        "n" => n as u128,
        "n log n" => (n as u128) * (n.ilog2() as u128),
        "n^2" => (n as u128) * (n as u128),
        "n^3" => (n as u128) * (n as u128) * (n as u128),
        _ => unreachable!(),
    }
}

// O(log budget) time, O(1) space
fn largest_n(growth: String, budget: i64) -> i64 {
    if growth == "2^n" {
        if budget < 2 {
            return 0;
        }
        return budget.ilog2() as i64;
    }
    let budget_u128 = budget as u128;
    if cost(&growth, 1) > budget_u128 {
        return 0;
    }
    let mut lo = 1;
    let mut hi = budget + 1;
    while lo < hi {
        let mid = (lo + hi + 1) / 2;
        if cost(&growth, mid) <= budget_u128 {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    lo
}

fn main() {
    println!("{:?}", largest_n(String::from("n^2"), 100));
}
