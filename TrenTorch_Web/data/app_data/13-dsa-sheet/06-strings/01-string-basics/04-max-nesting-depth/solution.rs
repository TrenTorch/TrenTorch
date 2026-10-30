// O(n) time, O(1) space
fn max_nesting_depth(s: String) -> i64 {
    let mut depth: i64 = 0;
    let mut best: i64 = 0;
    for ch in s.chars() {
        if ch == '(' {
            depth += 1;
            if depth > best {
                best = depth;
            }
        } else if ch == ')' {
            depth -= 1;
        }
    }
    best
}

fn main() {
    println!("{:?}", max_nesting_depth(String::from("(1+(2*3)+((8)/4))+1")));
}
