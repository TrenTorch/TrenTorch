fn remove_adjacent_duplicates(s: String) -> String {
    // O(n) time, O(n) space
    let mut stack = Vec::with_capacity(s.len());
    for ch in s.chars() {
        if let Some(&last) = stack.last() {
            if last == ch {
                stack.pop();
                continue;
            }
        }
        stack.push(ch);
    }
    stack.into_iter().collect()
}

fn main() {
    println!("{:?}", remove_adjacent_duplicates(String::from("abbaca")));
}
