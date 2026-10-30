// O(n) time, O(1) space
fn josephus(n: i64, k: i64) -> i64 {
    let mut position: i64 = 0;
    for m in 2..=n {
        position = (position + k) % m;
    }
    position + 1
}

fn main() {
    println!("{:?}", josephus(5, 2));
}
