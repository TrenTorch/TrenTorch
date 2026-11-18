use std::collections::VecDeque;

// O(1) amortized per operation, O(n) space (sliding window of hit times)
fn run_hit_counter(ops: Vec<String>) -> Vec<i64> {
    let mut window: VecDeque<i64> = VecDeque::new();
    let mut out: Vec<i64> = Vec::new();
    for op in ops.iter() {
        let mut it = op.split_whitespace();
        let kind = it.next().unwrap();
        let t: i64 = it.next().unwrap().parse().unwrap();
        if kind == "hit" {
            window.push_back(t);
        } else {
            while window.front().map_or(false, |&f| f <= t - 300) {
                window.pop_front();
            }
            out.push(window.len() as i64);
        }
    }
    out
}

fn main() {
    println!("{:?}", run_hit_counter(vec![String::from("hit 1"), String::from("hit 2"), String::from("hit 3"), String::from("count 4"), String::from("hit 300"), String::from("count 300"), String::from("count 301")]));
}
