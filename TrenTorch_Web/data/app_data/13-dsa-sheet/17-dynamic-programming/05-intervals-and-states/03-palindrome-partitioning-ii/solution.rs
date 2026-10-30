// O(n^2) time, O(n) space
fn min_cut_palindromes(s: String) -> i64 {
    let s = s.into_bytes();
    let n = s.len();
    if n == 0 {
        return 0;
    }
    // cuts[i]: fewest cuts for the first i letters
    let mut cuts: Vec<i64> = (-1..(n as i64)).collect();
    for centre in 0..n {
        let c = centre as isize;
        for (mut left, mut right) in [(c, c), (c, c + 1)] {
            while left >= 0 && (right as usize) < n && s[left as usize] == s[right as usize] {
                let l = left as usize;
                let r1 = (right + 1) as usize;
                if cuts[l] + 1 < cuts[r1] {
                    cuts[r1] = cuts[l] + 1;
                }
                left -= 1;
                right += 1;
            }
        }
    }
    cuts[n]
}

fn main() {
    println!("{:?}", min_cut_palindromes(String::from("aab")));
}
