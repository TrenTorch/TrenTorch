// O(k) time, O(1) space
fn step(mut x: i64) -> i64 {
    let mut total = 0;
    while x > 0 {
        let digit = x % 10;
        total += digit * digit;
        x /= 10;
    }
    total
}

fn happy_number(n: i64) -> bool {
    let mut slow = n;
    let mut fast = step(n);
    while fast != 1 && slow != fast {
        slow = step(slow);
        fast = step(step(fast));
    }
    fast == 1
}

fn main() {
    println!("{:?}", happy_number(19));
}
