// O(len(a) * len(b)) time, O(min(len(a), len(b))) space
fn edit_distance(a: String, b: String) -> i64 {
    let (mut a, mut b) = (a.into_bytes(), b.into_bytes());
    if b.len() > a.len() {
        std::mem::swap(&mut a, &mut b);
    }
    let m = b.len();
    let mut prev: Vec<i64> = (0..=m as i64).collect();
    for i in 1..=a.len() {
        let mut cur = vec![0i64; m + 1];
        cur[0] = i as i64;
        for j in 1..=m {
            cur[j] = if a[i - 1] == b[j - 1] {
                prev[j - 1]
            } else {
                1 + std::cmp::min(prev[j - 1], std::cmp::min(prev[j], cur[j - 1]))
            };
        }
        prev = cur;
    }
    prev[m]
}

fn main() {
    println!("{:?}", edit_distance(String::from("horse"), String::from("ros")));
}
