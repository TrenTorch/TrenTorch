use std::collections::VecDeque;

// O(n * L) time where L is the bit length (about 18 for n <= 200000), O(n * L) space
fn binary_numbers_up_to(n: i64) -> Vec<String> {
    let mut out: Vec<String> = Vec::new();
    let mut queue: VecDeque<String> = VecDeque::new();
    queue.push_back(String::from("1"));
    for _ in 0..n {
        let front = queue.pop_front().unwrap();
        queue.push_back(format!("{}0", front));
        queue.push_back(format!("{}1", front));
        out.push(front);
    }
    out
}

fn main() {
    println!("{:?}", binary_numbers_up_to(5));
}
