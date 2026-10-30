// O(n) time, O(1) space
fn remove_duplicate_letters(s: String) -> String {
    let n = s.len();
    // last occurrence index for each letter, -1 if not present
    let mut last = [-1i32; 26];
    for (i, ch) in s.chars().enumerate() {
        last[(ch as u8 - b'a') as usize] = i as i32;
    }
    let mut stack = Vec::with_capacity(26);
    let mut in_stack = [false; 26];
    for (i, ch) in s.chars().enumerate() {
        let idx = (ch as u8 - b'a') as usize;
        if in_stack[idx] {
            continue;
        }
        while let Some(&top) = stack.last() {
            let top_idx = (top as u8 - b'a') as usize;
            if top > ch && last[top_idx] > i as i32 {
                in_stack[top_idx] = false;
                stack.pop();
            } else {
                break;
            }
        }
        stack.push(ch);
        in_stack[idx] = true;
    }
    stack.into_iter().collect()
}

fn main() {
    println!("{:?}", remove_duplicate_letters(String::from("bcabc")));
}
