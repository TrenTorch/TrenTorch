// O(n) time, O(n) space
fn queue_with_two_stacks(ops: Vec<String>) -> Vec<i64> {
    let mut inbox = Vec::new();
    let mut outbox = Vec::new();
    let mut out = Vec::new();

    for op in ops {
        if op.starts_with("push") {
            let (_, num_str) = op.split_once(' ').unwrap();
            let x = num_str.parse::<i64>().unwrap();
            inbox.push(x);
        } else if op == "pop" {
            if outbox.is_empty() {
                while let Some(v) = inbox.pop() {
                    outbox.push(v);
                }
            }
            out.push(outbox.pop().unwrap());
        } else if op == "peek" {
            if outbox.is_empty() {
                while let Some(v) = inbox.pop() {
                    outbox.push(v);
                }
            }
            out.push(*outbox.last().unwrap());
        } else { // "empty"
            out.push(if inbox.is_empty() && outbox.is_empty() { 1 } else { 0 });
        }
    }
    out
}

fn main() {
    println!("{:?}", queue_with_two_stacks(vec![String::from("push 1"), String::from("push 2"), String::from("peek"), String::from("pop"), String::from("empty")]));
}
