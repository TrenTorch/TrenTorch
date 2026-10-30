// O(n) time, O(n) space
fn calculate_brackets(s: String) -> i64 {
    let mut stack: Vec<(i64, i64)> = Vec::new();
    let mut result: i64 = 0;
    let mut num: i64 = 0;
    let mut sign: i64 = 1;

    for ch in s.chars() {
        match ch {
            '0'..='9' => {
                num = num * 10 + (ch as i64 - '0' as i64);
            }
            '+' | '-' => {
                result += sign * num;
                num = 0;
                sign = if ch == '+' { 1 } else { -1 };
            }
            '(' => {
                stack.push((result, sign));
                result = 0;
                sign = 1;
            }
            ')' => {
                result += sign * num;
                num = 0;
                if let Some((saved_result, saved_sign)) = stack.pop() {
                    result = saved_result + saved_sign * result;
                }
            }
            _ => {} // ignore spaces and other characters
        }
    }

    result + sign * num
}

fn main() {
    println!("{:?}", calculate_brackets(String::from("(1+(4+5+2)-3)+(6+8)")));
}
