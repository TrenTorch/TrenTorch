// O(n) time (Manacher), O(n) space
fn longest_palindromic_substring(s: String) -> String {
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
    let mut best_len: usize = 0;
    let mut best_centre: usize = 0;
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
        if radius[i] > best_len {
            best_len = radius[i];
            best_centre = i;
        }
    }
    let start = (best_centre - best_len) / 2;
    String::from_utf8(bytes[start..start + best_len].to_vec()).unwrap()
}

fn main() {
    println!("{:?}", longest_palindromic_substring(String::from("babad")));
}
