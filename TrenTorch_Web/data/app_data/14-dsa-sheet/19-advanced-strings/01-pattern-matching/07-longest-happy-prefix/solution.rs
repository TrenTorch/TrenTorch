// O(n) time, O(n) space
fn longest_happy_prefix(s: String) -> String {
    let n = s.len();
    if n == 0 {
        return String::new();
    }
    let bytes = s.as_bytes();
    let mut pi = vec![0; n];
    let mut k = 0;
    for i in 1..n {
        while k > 0 && bytes[i] != bytes[k] {
            k = pi[k - 1];
        }
        if bytes[i] == bytes[k] {
            k += 1;
        }
        pi[i] = k;
    }
    let len = pi[n - 1];
    s[..len].to_string()
}

fn main() {
    println!("{:?}", longest_happy_prefix(String::from("level")));
}
