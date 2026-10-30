// O(len(s) * len(t)) time, O(len(t)) space
fn num_distinct(s: String, t: String) -> i64 {
    const MOD: i64 = 1_000_000_007;
    let s = s.into_bytes();
    let t = t.into_bytes();
    let mut row = vec![0i64; t.len() + 1];
    row[0] = 1;
    for &ch in &s {
        for j in (1..=t.len()).rev() {
            if t[j - 1] == ch {
                row[j] = (row[j] + row[j - 1]) % MOD;
            }
        }
    }
    row[t.len()]
}

fn main() {
    println!("{:?}", num_distinct(String::from("rabbbit"), String::from("rabbit")));
}
