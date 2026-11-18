// O(n) time, O(1) space where n = len(s) + len(t)
fn min_window(s: String, t: String) -> String {
    if t.is_empty() {
        return String::new();
    }
    let s_bytes = s.as_bytes();
    let t_bytes = t.as_bytes();
    let mut need = [0; 256];
    let mut missing = 0;
    for &b in t_bytes {
        if need[b as usize] == 0 {
            missing += 1;
        }
        need[b as usize] += 1;
    }
    let mut have = [0; 256];
    let mut left = 0;
    let mut best_start = 0;
    let mut best_len = s_bytes.len() + 1;
    for right in 0..s_bytes.len() {
        let b = s_bytes[right];
        have[b as usize] += 1;
        if need[b as usize] > 0 && have[b as usize] == need[b as usize] {
            missing -= 1;
        }
        while missing == 0 {
            let window_len = right - left + 1;
            if window_len < best_len {
                best_start = left;
                best_len = window_len;
            }
            let gone = s_bytes[left];
            have[gone as usize] -= 1;
            if need[gone as usize] > 0 && have[gone as usize] < need[gone as usize] {
                missing += 1;
            }
            left += 1;
        }
    }
    if best_len <= s_bytes.len() {
        String::from_utf8(s_bytes[best_start..best_start + best_len].to_vec()).unwrap()
    } else {
        String::new()
    }
}

fn main() {
    println!("{:?}", min_window(String::from("ADOBECODEBANC"), String::from("ABC")));
}
