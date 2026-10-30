// O(1) time, O(1) space
fn is_power_of_two(n: i64) -> bool {
    n > 0 && (n & (n - 1)) == 0
}

fn main() {
    println!("{:?}", is_power_of_two(16));
}
