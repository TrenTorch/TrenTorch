// O(n) time, O(1) space
fn min_add_to_make_valid(s: String) -> i64 {
    let mut open_count = 0i64;
    let mut need = 0i64;
    for ch in s.chars() {
        if ch == '(' {
            open_count += 1;
        } else if open_count > 0 {
            open_count -= 1;
        } else {
            need += 1;
        }
    }
    need + open_count
}

fn main() {
    println!("{:?}", min_add_to_make_valid(String::from("())")));
}
