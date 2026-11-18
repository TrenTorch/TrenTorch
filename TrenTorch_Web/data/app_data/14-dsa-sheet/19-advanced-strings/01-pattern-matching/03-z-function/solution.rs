// O(n) time, O(n) space
fn z_function(s: String) -> Vec<i64> {
    let s = s.into_bytes();
    let n = s.len();
    let mut z = vec![0usize; n];
    let mut left = 0usize;
    let mut right = 0usize;
    for i in 1..n {
        if i < right {
            z[i] = std::cmp::min(right - i, z[i - left]);
        }
        while i + z[i] < n && s[z[i]] == s[i + z[i]] {
            z[i] += 1;
        }
        if i + z[i] > right {
            left = i;
            right = i + z[i];
        }
    }
    z.into_iter().map(|x| x as i64).collect()
}

fn main() {
    println!("{:?}", z_function(String::from("aabxaab")));
}
