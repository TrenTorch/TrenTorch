// O(n) time, O(n) space
fn evaluate_rpn(tokens: Vec<String>) -> i64 {
    let mut stack = Vec::with_capacity(tokens.len());
    for token in tokens {
        match token.as_str() {
            "+" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a + b);
            }
            "-" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a - b);
            }
            "*" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a * b);
            }
            "/" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a / b); // truncates toward zero
            }
            _ => {
                stack.push(token.parse().unwrap());
            }
        }
    }
    stack[0]
}

fn main() {
    println!("{:?}", evaluate_rpn(vec![String::from("2"), String::from("1"), String::from("+"), String::from("3"), String::from("*")]));
}
