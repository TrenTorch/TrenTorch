// O(total ops) time (each step moves at most k positions), O(total visits) space
fn run_browser_history(homepage: String, ops: Vec<String>) -> Vec<String> {
    let mut history: Vec<String> = vec![homepage];
    let mut index: usize = 0;
    let mut out: Vec<String> = Vec::new();
    for op in ops.iter() {
        let mut it = op.split_whitespace();
        let kind = it.next().unwrap();
        let arg = it.next().unwrap();
        if kind == "visit" {
            history.truncate(index + 1);
            history.push(arg.to_string());
            index += 1;
        } else if kind == "back" {
            let k: usize = arg.parse().unwrap();
            index = index.saturating_sub(k);
            out.push(history[index].clone());
        } else {
            let k: usize = arg.parse().unwrap();
            index = std::cmp::min(history.len() - 1, index + k);
            out.push(history[index].clone());
        }
    }
    out
}

fn main() {
    println!("{:?}", run_browser_history(String::from("a"), vec![String::from("visit b"), String::from("visit c"), String::from("back 1"), String::from("back 5"), String::from("forward 1"), String::from("visit d"), String::from("forward 3")]));
}
