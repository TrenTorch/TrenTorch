// O(1) per operation, O(n) time overall, O(n) space
fn min_stack(ops: Vec<String>) -> Vec<i64> {
    let mut values: Vec<i64> = Vec::new();
    let mut mins: Vec<i64> = Vec::new();
    let mut out: Vec<i64> = Vec::new();
    for op in &ops {
        let op = op.as_str();
        if op.starts_with("push") {
            let x: i64 = op.split_whitespace().nth(1).unwrap().parse().unwrap();
            values.push(x);
            let m = match mins.last() {
                Some(&top) => top.min(x),
                None => x,
            };
            mins.push(m);
        } else if op == "pop" {
            values.pop();
            mins.pop();
        } else if op == "top" {
            out.push(*values.last().unwrap());
        } else {
            out.push(*mins.last().unwrap());
        }
    }
    out
}

fn main() {
    println!(
        "{:?}",
        min_stack(vec![
            String::from("push 5"),
            String::from("push 3"),
            String::from("get_min"),
            String::from("pop"),
            String::from("top"),
            String::from("get_min"),
        ])
    );
}
