// O(n^2 * log(n!)) time for bignum multiplication, O(d) space where d is the digit count of n!
fn factorial_digit_sum(n: i64) -> i64 {
    const BASE: u64 = 1_000_000_000;
    let mut limbs: Vec<u64> = vec![1];
    let mut k: u64 = 2;
    while k <= (n as u64) {
        let mut carry: u64 = 0;
        for limb in limbs.iter_mut() {
            let cur = *limb * k + carry;
            *limb = cur % BASE;
            carry = cur / BASE;
        }
        while carry > 0 {
            limbs.push(carry % BASE);
            carry /= BASE;
        }
        k += 1;
    }
    let mut sum: i64 = 0;
    for limb in &limbs {
        let mut v = *limb;
        while v > 0 {
            sum += (v % 10) as i64;
            v /= 10;
        }
    }
    sum
}

fn main() {
    println!("{:?}", factorial_digit_sum(10));
}
