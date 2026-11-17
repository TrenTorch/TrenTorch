// O(n) time, O(1) space
fn roman_to_integer(s: String) -> i64 {
    fn value(ch: char) -> i64 {
        match ch {
            'I' => 1,
            'V' => 5,
            'X' => 10,
            'L' => 50,
            'C' => 100,
            'D' => 500,
            'M' => 1000,
            _ => 0,
        }
    }

    let bytes = s.as_bytes();
    let mut total: i64 = 0;
    let len = bytes.len();

    for i in 0..len {
        let cur = value(bytes[i] as char);
        if i + 1 < len && cur < value(bytes[i + 1] as char) {
            total -= cur;
        } else {
            total += cur;
        }
    }
    total
}

fn main() {
    println!("{:?}", roman_to_integer(String::from("III")));
}
