// O(n) time, O(n) space
fn smallest_rotation(s: String) -> String {
    let n = s.len();
    if n == 0 {
        return String::new();
    }
    let s_bytes = s.as_bytes();
    let mut i = 0;
    let mut j = 1;
    let mut k = 0;
    while i < n && j < n && k < n {
        let a = s_bytes[(i + k) % n];
        let b = s_bytes[(j + k) % n];
        if a == b {
            k += 1;
            continue;
        }
        if a > b {
            i += k + 1;
        } else {
            j += k + 1;
        }
        if i == j {
            j += 1;
        }
        k = 0;
    }
    let start = std::cmp::min(i, j);
    format!("{}{}", &s[start..], &s[..start])
}

fn main() {
    println!("{:?}", smallest_rotation(String::from("bca")));
}
