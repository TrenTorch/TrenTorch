// O(n) time, O(n) space
fn count_bits_up_to(n: i64) -> Vec<i64> {
    let n_usize = n as usize;
    let mut bits = vec![0i64; n_usize + 1];
    for i in 1..=n_usize {
        bits[i] = bits[i >> 1] + ((i & 1) as i64);
    }
    bits
}

fn main() {
    println!("{:?}", count_bits_up_to(5));
}
