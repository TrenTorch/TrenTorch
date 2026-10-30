// O(1) time, O(1) space
fn reverse_bits(n: i64) -> i64 {
    let mut n = n;
    let mut result: i64 = 0;
    for _ in 0..32 {
        result = (result << 1) | (n & 1);
        n >>= 1;
    }
    result
}

fn main() {
    println!("{:?}", reverse_bits(1));
}
