use std::collections::HashMap;

// O(log m) per get where m is the number of sets on that key, O(total ops) space
fn run_time_map(ops: Vec<String>) -> Vec<String> {
    let mut store: HashMap<String, Vec<(i64, String)>> = HashMap::new();
    let mut out: Vec<String> = Vec::new();
    for op in ops.iter() {
        let parts: Vec<&str> = op.split_whitespace().collect();
        if parts[0] == "set" {
            let t: i64 = parts[3].parse().unwrap();
            store
                .entry(parts[1].to_string())
                .or_insert_with(Vec::new)
                .push((t, parts[2].to_string()));
        } else {
            let t: i64 = parts[2].parse().unwrap();
            let answer = match store.get(parts[1]) {
                Some(list) => {
                    let i = list.partition_point(|(ts, _)| *ts <= t);
                    if i > 0 {
                        list[i - 1].1.clone()
                    } else {
                        String::new()
                    }
                }
                None => String::new(),
            };
            out.push(answer);
        }
    }
    out
}

fn main() {
    println!("{:?}", run_time_map(vec![String::from("set love high 10"), String::from("get love 10"), String::from("get love 15"), String::from("set love low 20"), String::from("get love 15"), String::from("get love 25"), String::from("get love 5")]));
}
