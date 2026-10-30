// O(n log n) time, O(n) space
fn min_platforms(mut arrivals: Vec<i64>, mut departures: Vec<i64>) -> i64 {
    arrivals.sort_unstable();
    departures.sort_unstable();
    let n = arrivals.len();
    let mut current = 0;
    let mut best = 0;
    let mut i = 0;
    let mut j = 0;
    while i < n {
        if arrivals[i] <= departures[j] {
            current += 1;
            if current > best {
                best = current;
            }
            i += 1;
        } else {
            current -= 1;
            j += 1;
        }
    }
    best
}

fn main() {
    println!("{:?}", min_platforms(vec![900, 940, 950, 1100, 1500, 1800], vec![910, 1200, 1120, 1130, 1900, 2000]));
}
