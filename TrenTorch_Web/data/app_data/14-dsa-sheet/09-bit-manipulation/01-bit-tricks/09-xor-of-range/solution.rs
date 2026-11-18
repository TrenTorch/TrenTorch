// O(1) time, O(1) space
fn xor_of_range(left: i64, right: i64) -> i64 {
    fn prefix(n: i64) -> i64 {
        if n < 0 {
            return 0;
        }
        match n % 4 {
            0 => n,
            1 => 1,
            2 => n + 1,
            _ => 0,
        }
    }
    prefix(right) ^ prefix(left - 1)
}

fn main() {
    println!("{:?}", xor_of_range(3, 9));
}
