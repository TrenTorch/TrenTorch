// O(1) time, O(1) space
fn swap_odd_even_bits(n: i64) -> i64 {
    ((n & 0x5555_5555) << 1) | ((n & 0xAAAA_AAAA) >> 1)
}

fn main() {
    println!("{:?}", swap_odd_even_bits(10));
}
