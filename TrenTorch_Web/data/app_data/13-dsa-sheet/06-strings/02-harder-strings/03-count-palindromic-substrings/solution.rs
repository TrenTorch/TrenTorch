// O(n) time (Manacher), O(n) space
fn count_palindromic_substrings(s: String) -> i64 {
    let bytes = s.as_bytes();
    let mut t: Vec<u8> = Vec::with_capacity(2 * bytes.len() + 1);
    t.push(b'#');
    for &c in bytes {
        t.push(c);
        t.push(b'#');
    }
    let n = t.len();
    let mut radius: Vec<usize> = vec![0; n];
    let mut centre: usize = 0;
    let mut right: usize = 0;
    for i in 0..n {
        if i < right {
            radius[i] = std::cmp::min(right - i, radius[2 * centre - i]);
        }
        while i >= radius[i] + 1
            && i + radius[i] + 1 < n
            && t[i - radius[i] - 1] == t[i + radius[i] + 1]
        {
            radius[i] += 1;
        }
        if i + radius[i] > right {
            centre = i;
            right = i + radius[i];
        }
    }
    let mut total: i64 = 0;
    for &r in &radius {
        total += ((r + 1) / 2) as i64;
    }
    total
}

fn main() {
    println!("{:?}", count_palindromic_substrings(String::from("abc")));
}
