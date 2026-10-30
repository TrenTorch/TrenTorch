// O(n) time, O(1) additional space
fn largest_odd_number(num: String) -> String {
    let bytes = num.as_bytes();
    for i in (0..bytes.len()).rev() {
        match bytes[i] {
            b'1' | b'3' | b'5' | b'7' | b'9' => {
                return num[..=i].to_string();
            }
            _ => {}
        }
    }
    String::new()
}

fn main() {
    println!("{:?}", largest_odd_number(String::from("52")));
}
