// O(1) time, O(1) space
fn longest_ones_after_flip(n: i64) -> i64 {
    let mut best = 0;
    let mut current = 0;
    let mut previous = 0;
    for i in 0..32 {
        if (n >> i) & 1 == 1 {
            current += 1;
        } else {
            previous = current;
            current = 0;
        }
        best = std::cmp::max(best, previous + current + 1);
    }
    std::cmp::min(best, 32)
}

fn main() {
    println!("{:?}", longest_ones_after_flip(1775));
}
