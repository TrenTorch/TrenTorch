// O(n^2) time, O(n^2) space
fn palindrome_partitions(s: String) -> Vec<Vec<String>> {
    let n = s.len();
    let bytes = s.as_bytes();

    // precompute palindrome table
    let mut pal = vec![vec![false; n]; n];
    for length in 1..=n {
        for i in 0..=n - length {
            let j = i + length - 1;
            pal[i][j] = bytes[i] == bytes[j]
                && (length <= 2 || pal[i + 1][j - 1]);
        }
    }

    fn go(
        start: usize,
        n: usize,
        s: &str,
        pal: &Vec<Vec<bool>>,
        pieces: &mut Vec<String>,
        out: &mut Vec<Vec<String>>,
    ) {
        if start == n {
            out.push(pieces.clone());
            return;
        }
        for j in start..n {
            if pal[start][j] {
                pieces.push(s[start..j + 1].to_string());
                go(j + 1, n, s, pal, pieces, out);
                pieces.pop();
            }
        }
    }

    let mut out: Vec<Vec<String>> = Vec::new();
    let mut pieces: Vec<String> = Vec::new();
    go(0, n, &s, &pal, &mut pieces, &mut out);
    out
}

fn main() {
    println!("{:?}", palindrome_partitions(String::from("aab")));
}
