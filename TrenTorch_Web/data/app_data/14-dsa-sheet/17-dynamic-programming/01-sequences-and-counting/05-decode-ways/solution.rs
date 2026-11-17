// O(n) time, O(1) space
fn num_decodings(s: String) -> i64 {
    const MODULUS: i64 = 1_000_000_007;
    let bytes = s.as_bytes();
    let mut a: i64 = 1;
    let mut b: i64 = 1;
    for i in 1..=bytes.len() {
        let mut now: i64 = 0;
        if bytes[i - 1] != b'0' {
            now += b;
        }
        if i >= 2 {
            let two = &bytes[i - 2..i];
            if two >= &b"10"[..] && two <= &b"26"[..] {
                now += a;
            }
        }
        a = b;
        b = now % MODULUS;
    }
    if bytes.is_empty() {
        0
    } else {
        b % MODULUS
    }
}

fn main() {
    println!("{:?}", num_decodings(String::from("12")));
}
