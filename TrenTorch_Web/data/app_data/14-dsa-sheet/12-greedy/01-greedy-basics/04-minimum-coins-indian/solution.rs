// O(1) time, O(1) space
fn fewest_notes(amount: i64) -> i64 {
    let mut total = 0;
    let mut amount = amount;
    for &value in &[2000, 500, 100, 50, 20, 10, 5, 2, 1] {
        total += amount / value;
        amount %= value;
    }
    total
}

fn main() {
    println!("{:?}", fewest_notes(70));
}
