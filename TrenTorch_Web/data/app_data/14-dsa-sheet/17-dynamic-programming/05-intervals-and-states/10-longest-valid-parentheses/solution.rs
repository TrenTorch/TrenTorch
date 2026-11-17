// O(n) time, O(1) space
fn longest_valid_parentheses(s: String) -> i64 {
    let mut best: i64 = 0;
    let mut left: i64 = 0;
    let mut right: i64 = 0;

    // Left-to-right pass: '(' is opener
    for ch in s.chars() {
        if ch == '(' {
            left += 1;
        } else {
            right += 1;
        }
        if left == right {
            best = best.max(2 * left);
        } else if right > left {
            left = 0;
            right = 0;
        }
    }

    // Right-to-left pass: ')' is opener
    left = 0;
    right = 0;
    for ch in s.chars().rev() {
        if ch == ')' {
            left += 1;
        } else {
            right += 1;
        }
        if left == right {
            best = best.max(2 * left);
        } else if right > left {
            left = 0;
            right = 0;
        }
    }

    best
}

fn main() {
    println!("{:?}", longest_valid_parentheses(String::from(")()())")));
}
