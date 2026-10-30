use std::collections::HashMap;

// O(n) time, O(alphabet) space
fn character_replacement(s: String, k: i64) -> i64 {
    let chars: Vec<char> = s.chars().collect();
    let n = chars.len();
    let mut count: HashMap<char, usize> = HashMap::new();
    let mut left: usize = 0;
    let mut max_count: usize = 0;
    for right in 0..n {
        let c = count.entry(chars[right]).or_insert(0);
        *c += 1;
        if *c > max_count {
            max_count = *c;
        }
        let window_len = (right - left + 1) as i64;
        if window_len - (max_count as i64) > k {
            let l = chars[left];
            *count.get_mut(&l).unwrap() -= 1;
            left += 1;
        }
    }
    (n - left) as i64
}

fn main() {
    println!("{:?}", character_replacement(String::from("AABABBA"), 1));
}
