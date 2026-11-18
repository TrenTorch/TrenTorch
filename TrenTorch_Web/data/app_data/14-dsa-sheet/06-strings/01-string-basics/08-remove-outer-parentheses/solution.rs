// O(n) time, O(n) space
fn remove_outer_parentheses(s: String) -> String {
    let mut out = String::new();
    let mut depth: i64 = 0;
    for ch in s.chars() {
        if ch == '(' {
            if depth > 0 {
                out.push(ch);
            }
            depth += 1;
        } else {
            depth -= 1;
            if depth > 0 {
                out.push(ch);
            }
        }
    }
    out
}

fn main() {
    println!("{:?}", remove_outer_parentheses(String::from("(()())(())")));
}
