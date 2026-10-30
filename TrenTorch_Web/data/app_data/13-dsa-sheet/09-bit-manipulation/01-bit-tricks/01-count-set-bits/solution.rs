// O(k) time where k is number of set bits (≤ 62), O(1) space
fn count_set_bits(n: i64) -> i64 {
    let mut n = n;
    let mut count = 0;
    while n != 0 {
        n &= n - 1;
        count += 1;
    }
    count
}

fn main() {
    println!("{:?}", count_set_bits(13));
}
