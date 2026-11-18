// O(amount * k) time, O(amount) space (k = number of coin values)
fn coin_change(coins: Vec<i64>, amount: i64) -> i64 {
    let amt = amount as usize;
    let inf = i64::MAX / 2;
    let mut best = vec![inf; amt + 1];
    best[0] = 0;
    for a in 1..=amt {
        for &c in &coins {
            if c <= a as i64 {
                let prev = best[a - c as usize];
                if prev + 1 < best[a] {
                    best[a] = prev + 1;
                }
            }
        }
    }
    if best[amt] != inf {
        best[amt]
    } else {
        -1
    }
}

fn main() {
    println!("{:?}", coin_change(vec![1, 2, 5], 11));
}
