// O(n) time, O(1) space

fn solve(s: &[u8], k: usize, lo: usize, hi: usize) -> usize {
    if hi - lo < k {
        return 0;
    }
    let mut counts = [0; 26];
    for &b in &s[lo..hi] {
        counts[(b - b'a') as usize] += 1;
    }
    let mut rare = [false; 26];
    let mut has_rare = false;
    for i in 0..26 {
        if counts[i] > 0 && counts[i] < k {
            rare[i] = true;
            has_rare = true;
        }
    }
    if !has_rare {
        return hi - lo;
    }
    let mut best = 0;
    let mut start = lo;
    for i in lo..=hi {
        if i == hi || rare[(s[i] - b'a') as usize] {
            best = best.max(solve(s, k, start, i));
            start = i + 1;
        }
    }
    best
}

fn longest_substring_k_repeating(s: String, k: i64) -> i64 {
    let k = k as usize;
    let bytes = s.as_bytes();
    solve(bytes, k, 0, bytes.len()) as i64
}

fn main() {
    println!("{:?}", longest_substring_k_repeating(String::from("aaabb"), 3));
}
