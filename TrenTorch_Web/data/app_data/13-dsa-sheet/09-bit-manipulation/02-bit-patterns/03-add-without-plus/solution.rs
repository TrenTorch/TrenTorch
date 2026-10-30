// O(1) time, O(1) space
fn bit_add(a: i64, b: i64) -> i64 {
    const MASK: i64 = 0xFFFFFFFF;
    let mut a = a & MASK;
    let mut b = b & MASK;
    while b != 0 {
        let sum = (a ^ b) & MASK;
        let carry = ((a & b) << 1) & MASK;
        a = sum;
        b = carry;
    }
    if a >= (1 << 31) {
        a - (1 << 32)
    } else {
        a
    }
}

fn main() {
    println!("{:?}", bit_add(1, 2));
}
