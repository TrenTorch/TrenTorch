// O(n + m) time, O(m) space
fn count_overlapping(text: String, pattern: String) -> i64 {
    let text_bytes = text.as_bytes();
    let pattern_bytes = pattern.as_bytes();
    let m = pattern_bytes.len();
    if m == 0 {
        return 0;
    }
    let mut fail = vec![0; m];
    let mut k = 0;
    for i in 1..m {
        while k > 0 && pattern_bytes[i] != pattern_bytes[k] {
            k = fail[k - 1];
        }
        if pattern_bytes[i] == pattern_bytes[k] {
            k += 1;
        }
        fail[i] = k;
    }
    let mut count = 0;
    k = 0;
    for &ch in text_bytes {
        while k > 0 && ch != pattern_bytes[k] {
            k = fail[k - 1];
        }
        if ch == pattern_bytes[k] {
            k += 1;
        }
        if k == m {
            count += 1;
            k = fail[k - 1];
        }
    }
    count as i64
}

fn main() {
    println!("{:?}", count_overlapping(String::from("aaaa"), String::from("aa")));
}
