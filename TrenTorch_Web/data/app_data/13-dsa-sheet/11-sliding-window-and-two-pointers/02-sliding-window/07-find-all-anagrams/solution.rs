// O(n) time (26-letter count arrays), O(1) extra space besides the output
fn find_anagrams(s: String, p: String) -> Vec<i64> {
    let sb = s.as_bytes();
    let pb = p.as_bytes();
    let n = sb.len();
    let m = pb.len();
    let mut out: Vec<i64> = Vec::new();
    if m == 0 || m > n {
        return out;
    }
    let mut need = [0i64; 26];
    let mut window = [0i64; 26];
    for &ch in pb {
        need[(ch - b'a') as usize] += 1;
    }
    for i in 0..n {
        window[(sb[i] - b'a') as usize] += 1;
        if i >= m {
            window[(sb[i - m] - b'a') as usize] -= 1;
        }
        if i + 1 >= m && window == need {
            out.push((i + 1 - m) as i64);
        }
    }
    out
}

fn main() {
    println!("{:?}", find_anagrams(String::from("cbaebabacd"), String::from("abc")));
}
