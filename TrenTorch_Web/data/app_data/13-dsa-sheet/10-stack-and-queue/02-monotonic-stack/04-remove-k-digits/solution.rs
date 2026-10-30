// O(n) time, O(n) space
fn remove_k_digits(num: String, k: i64) -> String {
    let mut k = k as usize;
    let mut stack: Vec<char> = Vec::with_capacity(num.len());
    for ch in num.chars() {
        while k > 0 && !stack.is_empty() && *stack.last().unwrap() > ch {
            stack.pop();
            k -= 1;
        }
        stack.push(ch);
    }
    if k > 0 {
        stack.truncate(stack.len() - k);
    }
    let result: String = stack.into_iter().collect();
    let trimmed = result.trim_start_matches('0');
    if trimmed.is_empty() {
        "0".to_string()
    } else {
        trimmed.to_string()
    }
}

fn main() {
    println!("{:?}", remove_k_digits(String::from("1432219"), 3));
}
