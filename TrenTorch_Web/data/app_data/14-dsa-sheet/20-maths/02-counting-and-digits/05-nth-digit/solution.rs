// O(log n) time, O(1) space
fn nth_digit(n: i64) -> i64 {
    let mut n = n;
    let mut length: i64 = 1;
    let mut count: i64 = 9;
    let mut start: i64 = 1;
    while n > length * count {
        n -= length * count;
        length += 1;
        count *= 10;
        start *= 10;
    }
    let number = start + (n - 1) / length;
    let idx = ((n - 1) % length) as usize;
    let divisor = 10_i64.pow((length - 1 - idx as i64) as u32);
    ((number / divisor) % 10) as i64
}

fn main() {
    println!("{:?}", nth_digit(11));
}
