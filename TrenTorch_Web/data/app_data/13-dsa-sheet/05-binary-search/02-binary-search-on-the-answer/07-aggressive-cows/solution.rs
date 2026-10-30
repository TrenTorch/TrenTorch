// O(n log D) time, O(1) extra space (aside from sorting)
fn aggressive_cows(stalls: Vec<i64>, cows: i64) -> i64 {
    let mut s = stalls;
    s.sort_unstable();

    fn can_place(positions: &Vec<i64>, distance: i64, cows: i64) -> bool {
        let mut placed = 1i64;
        let mut last = positions[0];
        for &pos in positions.iter().skip(1) {
            if pos - last >= distance {
                placed += 1;
                last = pos;
                if placed >= cows {
                    return true;
                }
            }
        }
        placed >= cows
    }

    let mut lo = 1i64;
    let mut hi = s[s.len() - 1] - s[0];
    while lo < hi {
        let mid = (lo + hi + 1) / 2;
        if can_place(&s, mid, cows) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    lo
}

fn main() {
    println!("{:?}", aggressive_cows(vec![1, 2, 4, 8, 9], 3));
}
