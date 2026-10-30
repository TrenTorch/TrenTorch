// O(n) time, O(1) space
fn check_valid_string(s: String) -> bool {
    let mut lo = 0i64;
    let mut hi = 0i64;
    for ch in s.chars() {
        match ch {
            '(' => {
                lo += 1;
                hi += 1;
            }
            ')' => {
                lo -= 1;
                hi -= 1;
            }
            '*' => {
                lo -= 1;
                hi += 1;
            }
            _ => {}
        }
        if hi < 0 {
            return false;
        }
        if lo < 0 {
            lo = 0;
        }
    }
    lo == 0
}

fn main() {
    println!("{:?}", check_valid_string(String::from("(*)")));
}
