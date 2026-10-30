use std::iter::once;

// O(n) time, O(1) space
fn calculate(s: String) -> i64 {
    let mut total = 0i64;
    let mut last = 0i64;
    let mut num = 0i64;
    let mut op = '+';
    for ch in s.chars().chain(once('+')) {
        if ch.is_ascii_digit() {
            num = num * 10 + (ch as u8 - b'0') as i64;
        } else if ch != ' ' {
            match op {
                '+' => {
                    total += last;
                    last = num;
                }
                '-' => {
                    total += last;
                    last = -num;
                }
                '*' => {
                    last *= num;
                }
                '/' => {
                    last /= num;
                }
                _ => {}
            }
            op = ch;
            num = 0;
        }
    }
    total + last
}

fn main() {
    println!("{:?}", calculate(String::from("3+2*2")));
}
