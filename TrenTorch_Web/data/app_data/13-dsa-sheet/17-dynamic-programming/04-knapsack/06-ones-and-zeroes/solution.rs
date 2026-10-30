// O(L * m * n) time, O(m * n) space
fn find_max_form(strs: Vec<String>, m: i64, n: i64) -> i64 {
    let m_usize = m as usize;
    let n_usize = n as usize;
    let mut best = vec![vec![0; n_usize + 1]; m_usize + 1];
    for s in strs {
        let zeros = s.chars().filter(|&c| c == '0').count();
        let ones = s.len() - zeros;
        if zeros > m_usize || ones > n_usize {
            continue;
        }
        for z in (zeros..=m_usize).rev() {
            for o in (ones..=n_usize).rev() {
                let candidate = best[z - zeros][o - ones] + 1;
                if candidate > best[z][o] {
                    best[z][o] = candidate;
                }
            }
        }
    }
    best[m_usize][n_usize] as i64
}

fn main() {
    println!("{:?}", find_max_form(vec![String::from("10"), String::from("0001"), String::from("111001"), String::from("1"), String::from("0")], 5, 3));
}
