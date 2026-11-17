// O(k) time where k is number of set bits (≤ 31), O(1) space
fn bit_flips_to_convert(a: i64, b: i64) -> i64 {
    let mut diff = a ^ b;
    let mut count = 0;
    while diff != 0 {
        diff &= diff - 1;
        count += 1;
    }
    count
}

fn main() {
    println!("{:?}", bit_flips_to_convert(10, 7));
}
