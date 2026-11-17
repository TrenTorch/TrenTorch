// O(n) time, O(n) space
fn valid_brackets(s: String) -> bool {
    let mut stack = Vec::with_capacity(s.len());
    for ch in s.chars() {
        match ch {
            ')' => {
                if stack.pop() != Some('(') {
                    return false;
                }
            }
            ']' => {
                if stack.pop() != Some('[') {
                    return false;
                }
            }
            '}' => {
                if stack.pop() != Some('{') {
                    return false;
                }
            }
            '(' | '[' | '{' => stack.push(ch),
            _ => {}
        }
    }
    stack.is_empty()
}

fn main() {
    println!("{:?}", valid_brackets(String::from("()[]{}")));
}
