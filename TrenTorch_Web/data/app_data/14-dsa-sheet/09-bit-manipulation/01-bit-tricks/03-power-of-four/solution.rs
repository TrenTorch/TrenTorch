// O(1) time, O(1) space
fn is_power_of_four(n: i64) -> bool {
    n > 0 && n & (n - 1) == 0 && n & 0x5555555555555555 != 0
}

fn main() {
    println!("{:?}", is_power_of_four(16));
}
