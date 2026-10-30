// O(k * n) time, O(n) space where k is number of distinct permutations, n = s.len()
fn build(letters: &[char], left: &mut [usize], n: usize, prefix: &mut Vec<char>, out: &mut Vec<String>) {
    if prefix.len() == n {
        out.push(prefix.iter().collect());
        return;
    }
    for i in 0..letters.len() {
        if left[i] > 0 {
            left[i] -= 1;
            prefix.push(letters[i]);
            build(letters, left, n, prefix, out);
            prefix.pop();
            left[i] += 1;
        }
    }
}

fn distinct_permutations(s: String) -> Vec<String> {
    let mut freq = [0; 26];
    for c in s.chars() {
        freq[(c as u8 - b'a') as usize] += 1;
    }
    let mut letters = Vec::new();
    let mut left = Vec::new();
    for i in 0..26 {
        if freq[i] > 0 {
            letters.push((b'a' + i as u8) as char);
            left.push(freq[i]);
        }
    }
    let n = s.len();
    let mut prefix = Vec::new();
    let mut out = Vec::new();
    build(&letters, &mut left, n, &mut prefix, &mut out);
    out
}

fn main() {
    println!("{:?}", distinct_permutations(String::from("abc")));
}
